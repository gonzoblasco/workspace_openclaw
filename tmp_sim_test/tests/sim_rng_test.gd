extends SceneTree
var SimRNG = preload("res://sim/rng.gd")

func _init():
    var seed = 12345
    var rng1 = SimRNG.new(seed)
    var seq1 = []
    for i in range(1000):
        seq1.append(rng1.next_u32())
    var rng2 = SimRNG.new(seed)
    var seq2 = []
    for i in range(1000):
        seq2.append(rng2.next_u32())
    var same = true
    for i in range(1000):
        if seq1[i] != seq2[i]:
            same = false
            break
    if not same:
        push_error("Same seed produced different sequences")
        quit(1)
        return
    var rng3 = SimRNG.new(seed + 1)
    var diff = false
    for i in range(1000):
        if rng3.next_u32() != seq1[i]:
            diff = true
            break
    if not diff:
        push_error("Different seed produced identical sequence")
        quit(1)
        return
    print("RNG_OK")
    quit()

