import pytest
import libriscv._riscv as riscv


@pytest.mark.parametrize("raw_insn,exp_len", [
    pytest.param(0x4581, 2, id="c.li/int"),
    pytest.param(b"\x81\x45", 2, id="c.li"),
    pytest.param(0x02828613, 4, id="addi/int"),
    pytest.param(b"\x13\x86\x82\x02", 4, id="addi"),
])
def test_riscv_insn_length(raw_insn, exp_len):
    """
    test insn_length() function
    """
    assert riscv.insn_length(raw_insn) == exp_len


@pytest.mark.parametrize("raw_insn,exp_seq", [
    pytest.param(b'\x81\x45\x13\x86\x82\x02\x09\xa0', [0x4581, 0x02828613, 0xa009], id="c.li,addi,c.j"),
    pytest.param(b'\x81\x45\x13\x86\x82\x02\x09\xa0\x13', [0x4581, 0x02828613, 0xa009], id="c.li,addi,c.j,<part>"),
])
def test_riscv_insn_fetch_all(raw_insn, exp_seq):
    """
    test insn_fetch_all() function
    """
    seq = riscv.insn_fetch_all(raw_insn)
    assert seq == exp_seq


@pytest.mark.parametrize("raw_insn,exp_len", [
    pytest.param(b"\x81\x45", 2, id="c.li"),
    pytest.param(b"\x13\x86\x82\x02", 4, id="addi"),
])
def test_riscv_insn_t(raw_insn, exp_len):
    """
    test insn_t class construction and comparison
    """
    insn = riscv.insn_t(int.from_bytes(raw_insn, "little"))
    assert len(insn) == exp_len
    assert insn == int.from_bytes(raw_insn, "little")
    assert insn == raw_insn
    assert insn == riscv.insn_t(raw_insn)


@pytest.mark.parametrize("isa,priv,exp_xlen,exp_flags", [
    pytest.param("rv64imafdcv_zicsr_zifencei_zba_zbb_zbc_zbs", "msu", 64, (
        *(ord(bit) for bit in "IMAFDCV"),
        riscv.isa_extension_t.zba, riscv.isa_extension_t.zbb, riscv.isa_extension_t.zbc, riscv.isa_extension_t.zbs,
    ), id="rv64gcv_zicsr_zifencei_zba_zbb_zbc_zbs/msu"),
    pytest.param("rv32imafdc_zicsr_zifencei_zba_zbb_zbc_zbs", "msu", 32, (
        *(ord(bit) for bit in "IMAFDC"),
        riscv.isa_extension_t.zba, riscv.isa_extension_t.zbb, riscv.isa_extension_t.zbc, riscv.isa_extension_t.zbs,
    ), id="rv32gc_zicsr_zifencei_zba_zbb_zbc_zbs/msu"),
])
def test_riscv_isa_parser_t(isa, priv, exp_xlen, exp_flags):
    """
    test isa_parser_t class construction and membership
    """
    isa_parser = riscv.isa_parser_t(isa, priv)
    assert isa_parser.max_xlen == exp_xlen
    assert isa_parser.isa == isa
    assert all(f in isa_parser for f in exp_flags)


@pytest.mark.parametrize("raw_insn,exp_name,exp_mnemonic", [
    pytest.param(b"\x81\x45", "c.li", "c.li    a1, 0", id="c.li"),
    pytest.param(b"\x13\x86\x82\x02", "addi", "addi    a2, t0, 40", id="addi"),
])
def test_riscv_disassembler_t(raw_insn, exp_name, exp_mnemonic):
    """
    test riscv disassembler
    """
    isa_parser = riscv.isa_parser_t("rv64gcv_zicsr_zifencei_zba_zbb_zbc_zbs", "msu")
    disasm = riscv.disassembler_t(isa_parser)
    insn = riscv.insn_t(raw_insn)
    assert disasm.disassemble(insn) == exp_mnemonic
    assert disasm.lookup(insn) == insn
    assert disasm.lookup(insn).name == exp_name
