extends RefCounted
# Pure fixed-tick rules; no visuals, RNG, wall clock, or audio authority.
var tick := 0
var charge := 0
var score := 0
var recovery := 0
var state := "ready"
var previous_hold := false
var events: Array = []
var last := "Hold SPACE. Release near the gold mark."
const TARGET := 8
func emit(kind: String, data = {}) -> void:
 events.append({"tick": tick, "kind": kind, "data": data})
func step(held: bool, retry := false) -> void:
 tick += 1
 if retry:
  score = 0; charge = 0; recovery = 0; state = "ready"; previous_hold = false
  last = "Fresh lantern. Try again!"; emit("retry"); return
 if state == "lost" or state == "won":
  previous_hold = held; return
 if recovery > 0:
  recovery -= 1
  if held and not previous_hold:
   last = "Recovering - input acknowledged"; emit("blocked", {"reason":"recovery"})
  previous_hold = held; return
 if held:
  if not previous_hold:
   emit("windup"); last = "Gathering... release before the red edge."
  charge += 1; state = "charging"
  if charge >= 66:
   state = "lost"; last = "Overloaded! Press R - instant retry."; emit("overload")
 elif previous_hold and charge > 0:
  var gain := 1 if charge < 30 else (2 if charge < 48 else 3)
  score += gain; recovery = 18; state = "ready"
  last = ("SAFE +1" if gain == 1 else ("GOOD +2" if gain == 2 else "BRILLIANT +3"))
  emit("release", {"charge": charge, "gain": gain, "score": score}); charge = 0
  if score >= TARGET:
   state = "won";last = "Grove restored! Press R to replay.";emit("win")
 previous_hold = held
func snapshot() -> Array:
 return [tick,charge,score,recovery,state,previous_hold]
static func demo_input(n: int) -> Array:
 # Deliberate scripted demonstration: safe, brilliant, fail, retry, then win.
 var hold := (n>=20 and n<38) or (n>=85 and n<137) or (n>=175 and n<244) or (n>=285 and n<337) or (n>=385 and n<437) or (n>=485 and n<537)
 return [hold,n==260]
