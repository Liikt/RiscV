from binaryninja import CallingConvention


class RiscVWithoutFloats(CallingConvention):
    name = "RiscV"
    global_pointer_reg = 'gp'
    caller_saved_regs = (
        'ra',
        't0',
        't1',
        't2',
        't3',
        't4',
        't5',
        't6',
        'a0',
        'a1',
        'a2',
        'a3',
        'a4',
        'a5',
        'a6',
        'a7',
    )
    callee_saved_regs = (
        'sp',
        's0',
        's1',
        's2',
        's3',
        's4',
        's5',
        's6',
        's7',
        's8',
        's9',
        's10',
        's11',
    )

    int_arg_regs = ('a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7')
    int_return_reg = 'a0'
    high_int_return_reg = 'a1'

    float_arg_regs = ()
    float_return_arg = ''
    high_float_return_arg = ''

    implicitly_defined_regs = ('tp', 'gp')


class RiscVWithFloats(RiscVWithoutFloats):
    caller_saved_regs = (
        'ra',
        't0',
        't1',
        't2',
        't3',
        't4',
        't5',
        't6',
        'a0',
        'a1',
        'a2',
        'a3',
        'a4',
        'a5',
        'a6',
        'a7',
        'ft0',
        'ft1',
        'ft2',
        'ft3',
        'ft4',
        'ft5',
        'ft6',
        'ft7',
        'ft8',
        'ft9',
        'ft10',
        'ft11',
        'fa0',
        'fa1',
        'fa2',
        'fa3',
        'fa4',
        'fa5',
        'fa6',
        'fa7',
    )
    callee_saved_regs = (
        'sp',
        's0',
        's1',
        's2',
        's3',
        's4',
        's5',
        's6',
        's7',
        's8',
        's9',
        's10',
        's11',
        'fs0',
        'fs1',
        'fs2',
        'fs3',
        'fs4',
        'fs5',
        'fs6',
        'fs7',
        'fs8',
        'fs9',
        'fs10',
        'fs11',
    )

    float_arg_regs = ('fa0', 'fa1', 'fa2', 'fa3', 'fa4', 'fa5', 'fa6')
    float_return_arg = 'fa0'
    high_float_return_arg = 'fa1'