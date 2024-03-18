#include <vector>

#include <riscv/decode.h>
#include <riscv/disasm.h>
#include <riscv/isa_parser.h>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

insn_bits_t
insn_fetch_one(py::bytes data) {
  auto view = data.attr("__getitem__");
  auto from_bytes = py::int_().attr("from_bytes");
  int length = insn_length(view(0).cast<unsigned char>());
  auto insn = from_bytes(view(py::slice(0, length, 1)), "little");
  return insn.cast<insn_bits_t>();
}

std::vector<insn_bits_t>
insn_fetch_all(py::bytes data) {
  std::vector<insn_bits_t> sequence;
  auto view = data.attr("__getitem__");
  auto from_bytes = py::int_().attr("from_bytes");
  auto total = py::len(data);
  size_t offset = 0;
  while (offset < total) {
    int length = insn_length(view(offset).cast<unsigned char>());
    if (offset + length > total) {
      break;
    }
    auto insn = from_bytes(view(py::slice(offset, offset + length, 1)), "little");
    sequence.push_back(insn.cast<insn_bits_t>());
    offset += length;
  }
  return sequence;
}

PYBIND11_MODULE(_riscv, m) {
  m.doc() = "Python bindings of Spike RISC-V ISA Simulator (libriscv.so)";

  m.attr("MAX_INSN_LENGTH") = MAX_INSN_LENGTH;

  // guess instruction length from the least significant byte (insn_bits_t version)
  m.def("insn_length", [](insn_bits_t bits) -> int {
    return insn_length(bits);
  }, py::arg("bits"));

  // guess instruction length from the least significant byte (py::bytes version)
  m.def("insn_length", [](py::bytes data) -> int {
    auto view = data.attr("__getitem__");
    return insn_length(view(0).cast<unsigned char>());
  }, py::arg("data"));

  // fetch a single instruction from a byte sequence
  m.def("insn_fetch_all", &insn_fetch_all, py::arg("data"));

  py::enum_<isa_extension_t>(m, "isa_extension_t")
    .value("zba", isa_extension_t::EXT_ZBA)
    .value("zbb", isa_extension_t::EXT_ZBB)
    .value("zbc", isa_extension_t::EXT_ZBC)
    .value("zbs", isa_extension_t::EXT_ZBS)
    .export_values();

  py::enum_<impl_extension_t>(m, "impl_extension_t")
    .value("SV39", impl_extension_t::IMPL_MMU_SV39)
    .value("SV48", impl_extension_t::IMPL_MMU_SV48)
    .export_values();

  py::class_<isa_parser_t>(m, "isa_parser_t")
    .def(py::init<const char *, const char *>(), py::arg("isa"), py::arg("priv"))
    .def_property_readonly("max_xlen", &isa_parser_t::get_max_xlen)
    .def_property_readonly("max_isa", &isa_parser_t::get_max_isa)
    .def_property_readonly("isa", &isa_parser_t::get_isa_string)
    .def("__contains__", py::overload_cast<unsigned char>(&isa_parser_t::extension_enabled, py::const_), py::arg("ext"))
    .def("__contains__", py::overload_cast<isa_extension_t>(&isa_parser_t::extension_enabled, py::const_), py::arg("ext"))
    .def_property_readonly("extensions", &isa_parser_t::get_extensions);

  py::class_<insn_t>(m, "insn_t")
    .def(py::init<>())
    .def(py::init<insn_bits_t>(), py::arg("bits"))
    .def(py::init([](py::bytes bits) { return new insn_t(insn_fetch_one(bits)); }), py::arg("bits"))
    .def_property_readonly("bits", [](insn_t& self) {
      uint64_t bits = self.bits();
      return py::bytes(reinterpret_cast<const char *>(&bits), self.length());
    })
    .def("__len__", &insn_t::length)
    .def("__eq__", [](insn_t &self, insn_t &other) { return self.bits() == other.bits(); })
    .def("__eq__", [](insn_t &self, uint64_t other) { return self.bits() == other; })
    .def("__eq__", [](insn_t &self, py::bytes other) {
      uint64_t bits = self.bits();
      return py::bytes(reinterpret_cast<const char *>(&bits), self.length()).equal(other);
    });

  py::class_<disasm_insn_t>(m, "disasm_insn_t")
    .def_property_readonly("name", &disasm_insn_t::get_name)
    .def("__eq__", &disasm_insn_t::operator==);

  py::class_<disassembler_t>(m, "disassembler_t")
    .def(py::init<const isa_parser_t *>(), py::arg("isa"))
    .def("disassemble", &disassembler_t::disassemble)
    .def("lookup", &disassembler_t::lookup, py::return_value_policy::copy);
}
