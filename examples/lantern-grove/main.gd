extends Node2D
const Sim = preload("res://sim.gd")
var sim = Sim.new()
var courier: Texture2D
var tree: Texture2D
var grove: Texture2D
var font: Font
var held := false
var retry := false
var demo := false
var reduced := false
var clock := 0
var seen := 0
var pose_hold := 0
var burst := 0
var pulse := 0
var audio: AudioStreamPlayer
var capture_rows: Array=[]
func _ready() -> void:
 courier=load("res://assets/courier.png");tree=load("res://assets/tree.png")
 grove=load("res://assets/grove.png")
 font=ThemeDB.fallback_font
 audio=AudioStreamPlayer.new();audio.stream=load("res://assets/chime.wav");audio.volume_db=-15;add_child(audio)
 demo="--demo" in OS.get_cmdline_user_args()
 reduced="--reduced" in OS.get_cmdline_user_args()
func _input(event: InputEvent) -> void:
 if event is InputEventKey and not event.echo:
  if event.keycode==KEY_SPACE: held=event.pressed
  if event.pressed and event.keycode==KEY_R:retry=true
  if event.pressed and event.keycode==KEY_M:reduced=not reduced
  if event.pressed and event.keycode==KEY_ESCAPE:get_tree().quit()
func _physics_process(_dt: float) -> void:
 clock+=1
 var input=Sim.demo_input(clock-1) if demo else [held,retry]
 sim.step(input[0],input[1]);retry=false
 if pose_hold>0:pose_hold-=1
 if burst>0:burst-=1
 if pulse>0:pulse-=1
 while seen<sim.events.size():
  var e=sim.events[seen];seen+=1
  if e.kind=="release":
   pose_hold=5;burst=20;pulse=12;audio.play()
  elif e.kind=="overload":burst=15
  elif e.kind=="retry":pose_hold=0;burst=0;pulse=0
 capture_rows.append({"tick":clock,"state":sim.state,"score":sim.score,"pose_hold":pose_hold,"burst":burst,"world_clock":clock,"logical":sim.snapshot(),"optional_particles":0 if reduced else (12 if burst>0 else 0)})
 if demo and clock==600:
  var f=FileAccess.open("res://docs/"+("reduced-trace.json" if reduced else "capture-trace.json"),FileAccess.WRITE);f.store_string(JSON.stringify(capture_rows))
 queue_redraw()
func text(p: Vector2,s: String,size := 16,color := Color("e6efd4")) -> void:
 draw_string(font,p,s,HORIZONTAL_ALIGNMENT_LEFT,-1,size,color)
func _draw() -> void:
 draw_texture_rect(grove,Rect2(0,0,640,360),false)
 # Quiet overlay bands retain the scene's focal hierarchy.
 draw_rect(Rect2(0,0,640,57),Color(0.025,0.07,0.09,.82))
 text(Vector2(22,27),"LANTERN GROVE",23,Color("ffdea0"))
 text(Vector2(23,46),"Gather the forest's light. Restore the ancient lantern.",12,Color("b4d6cd"))
 text(Vector2(454,24),"LIGHT  %d / %d"%[sim.score,Sim.TARGET],21,Color("ffdea0"))
 text(Vector2(454,43),"M  gentler effects   R  retry",11,Color("b4d6cd"))
 if demo:text(Vector2(22,73),"SCRIPTED ENGINE CAPTURE",10,Color("aacbc5"))
 var q=minf(sim.charge/66.0,1.0)
 var center=Vector2(438,177)
 var danger=sim.state=="lost"
 var light_color=Color("ff916c") if danger else Color("ffe6a1")
 # The light is gathered INTO the visible shrine, not an unrelated floating target.
 draw_circle(center,14,Color(.92,.68,.25,.16+.15*q))
 draw_circle(center,4+q*8,light_color)
 draw_arc(center,23,-PI/2,-PI/2+q*TAU,48,Color("f9d77c"),2)
 if q>.88:
  draw_rect(Rect2(393,211,90,19),Color(.15,.05,.04,.9))
  text(Vector2(401,225),"TOO MUCH!",12,Color("ffad8e"))
 # Courier at human-readable scale; its feet meet the generated stone terrace.
 var squash=Vector2(1,1)
 if sim.state=="charging":squash=Vector2(1+.09*q,1-.09*q)
 elif pose_hold>0:squash=Vector2(.91,1.09)
 var size=Vector2(86,110)*squash
 draw_ellipse_shadow(Vector2(238,253),Vector2(31,4))
 draw_texture_rect(courier,Rect2(Vector2(238-size.x/2,253-size.y),size),false)
 if sim.state=="charging":
  for i in range(5):
   var u=fmod(clock*.015+i*.2,1.0)
   var start=Vector2(270,205)
   var point=start.lerp(center,u)+Vector2(0,-sin(u*PI)*24)
   draw_circle(point,1.5+q,Color("ffe6a1"))
 if not reduced:
  for i in range(15):
   var point=Vector2(fmod(i*43.0+clock*.12,620)+10,100+fmod(i*31.0,160)+sin(clock*.02+i)*4)
   draw_circle(point,1,Color(.97,.83,.44,.25+.3*maxf(0,sin(clock*.03+i))))
  if burst>0:
   for i in range(12):
    var angle=i*TAU/12
    var r=(20-burst)*2.0
    draw_circle(center+Vector2(cos(angle),sin(angle))*r,2,Color("ffe6a1"))
 # One compact instruction/status panel; the world remains visible behind it.
 draw_rect(Rect2(16,292,608,56),Color(.025,.075,.085,.94))
 draw_line(Vector2(16,292),Vector2(624,292),Color("658e7d"),1)
 text(Vector2(29,313),sim.last,16,Color("ffe1a0"))
 draw_rect(Rect2(29,326,300,7),Color("294945"))
 draw_rect(Rect2(29,326,300*q,7),Color("80d4b8") if q<.72 else Color("ffce74"))
 draw_line(Vector2(29+300*48.0/66,323),Vector2(29+300*48.0/66,337),Color("fff1ca"),2)
 text(Vector2(348,330),"SPACE hold / release    +1 / +2 / +3",12,Color("b4d6cd"))
 if sim.state=="won":
  draw_rect(Rect2(164,91,312,64),Color(.035,.14,.14,.96))
  draw_rect(Rect2(164,91,312,64),Color("c9b975"),false,1)
  text(Vector2(185,117),"THE GROVE IS ALIGHT",21,Color("ffdea0"))
  text(Vector2(187,140),"Lantern restored. R to gather again.",13,Color("c4ded3"))
func draw_ellipse_shadow(center: Vector2, size: Vector2) -> void:
 draw_set_transform(center,0,size)
 draw_circle(Vector2.ZERO,1,Color(0,.025,.02,.4))
 draw_set_transform(Vector2.ZERO)
