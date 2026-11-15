extends SceneTree
const Sim = preload("res://sim.gd")
var checks := 0
func check(ok: bool, why: String) -> void:
 checks += 1
 if not ok:
  push_error(why);quit(1);assert(false,why)
func _init() -> void:
 for duration in [1,29,30,47,48,65,66]:
  var boundary = Sim.new()
  for j in range(duration):boundary.step(true)
  boundary.step(false)
  var expected := 0 if duration==66 else (1 if duration<30 else (2 if duration<48 else 3))
  check(boundary.score==expected,"charge boundary "+str(duration))
 var safe = Sim.new()
 for i in range(18): safe.step(true)
 safe.step(false); check(safe.score==1,"safe reward")
 var perfect = Sim.new()
 for i in range(52): perfect.step(true)
 perfect.step(false);check(perfect.score==3,"risk rewarded")
 perfect.step(true);check(perfect.events[-1].kind=="blocked","blocked input acknowledged")
 var fail = Sim.new()
 for i in range(66): fail.step(true)
 check(fail.state=="lost" and fail.score==0,"overcharge fails")
 fail.step(false,true); check(fail.state=="ready" and fail.charge==0,"retry in one tick")
 var baseline = Sim.new();var reduced = Sim.new();var hashes: Array=[]
 for n in range(600):
  var input = Sim.demo_input(n)
  baseline.step(input[0],input[1]); reduced.step(input[0],input[1])
  # Presentation-only work at 30/60/120Hz must never call step again.
  for fps in [30,60,120]:
   var before = reduced.snapshot().duplicate()
   for j in range(fps/30): var ignored = reduced.snapshot()
   check(before==reduced.snapshot(),"presentation changed state")
  check(baseline.snapshot()==reduced.snapshot(),"replay diverged")
  hashes.append(hash(baseline.snapshot()))
 check(baseline.state=="won" and baseline.score==9,"script reaches outcome")
 var report = {"driver":"Godot headless SceneTree", "engine":Engine.get_version_info().string,"checks":checks,"result":"pass","scripted_ticks":600,"outcome":baseline.state,"score":baseline.score,"events":baseline.events,"scope":"Pure fixed-tick rules. Presentation no-mutation check, not a real render-FPS benchmark; no human playtest."}
 var f=FileAccess.open("res://docs/sim-report.json",FileAccess.WRITE);f.store_string(JSON.stringify(report,"  "))
 print(JSON.stringify(report));quit(0)
