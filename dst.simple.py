def clear_dunder_slots(p, ex=[]):
    slots = p.copy()
    import re
    for slot_name in p.keys():
        m = re.search("^__(.+)__$", slot_name)
        if m and m.group(1) not in ex:
            del slots[slot_name]
    return slots


def dst_fill_slot(c, s, p):
    slot = c['slot']
    p = clear_dunder_slots(p)
    if p[slot]:
        s[slot] = p[slot]
    return s


def dst_update_slots(c, s, p):
    p = clear_dunder_slots(p)
    s.update(p)
    return s


def dst_default(c, s, p):
    s.clear()
    p = clear_dunder_slots(p)
    s.update(p)
    return s


def dst_fill_slot_yes_no(c, s, p):
    slot = c['slot']
    p = clear_dunder_slots(p, ["yes_no"])
    if p[slot]:
        s[slot] = p[slot]
    elif p['__yes_no__']:
        s[slot] = c[p['__yes_no__'][0].lower()]
    return s


def dst_update_slots_yes_no(c, s, p):
    slot = c['slot']
    p = clear_dunder_slots(p, ["yes_no"])
    s.update(p)
    if not p[slot] and p['__yes_no__']:
        s[slot] = c[p['__yes_no__'][0].lower()]
    return s


def get():
    return {
        'UPDATE_SLOTS_YES_NO': dst_update_slots_yes_no,
        'UPDATE_SLOTS': dst_update_slots,
        'FILL_SLOT': dst_fill_slot,
        'FILL_SLOT_YES_NO': dst_fill_slot_yes_no,
        'DEFAULT': dst_default,
        "TERMINATE": dst_default
    }