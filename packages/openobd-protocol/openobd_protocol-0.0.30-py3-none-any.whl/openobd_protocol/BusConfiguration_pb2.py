# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: openobd_protocol/BusConfiguration.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\'openobd_protocol/BusConfiguration.proto\x12\x1d\x63om.jifeline.OpenOBD.Protocol\"\xa5\x02\n\x10\x42usConfiguration\x12\x10\n\x08\x62us_name\x18\x01 \x01(\t\x12\x38\n\x07\x63\x61n_bus\x18\x02 \x01(\x0b\x32%.com.jifeline.OpenOBD.Protocol.CanBusH\x00\x12<\n\tkline_bus\x18\x03 \x01(\x0b\x32\'.com.jifeline.OpenOBD.Protocol.KlineBusH\x00\x12:\n\x06plus15\x18\x04 \x01(\x0b\x32(.com.jifeline.OpenOBD.Protocol.Plus15BusH\x00\x12:\n\x08\x64oip_bus\x18\x05 \x01(\x0b\x32&.com.jifeline.OpenOBD.Protocol.DoipBusH\x00\x42\x0f\n\rBusDefinition\"\x89\x02\n\x06\x43\x61nBus\x12\x10\n\x08pin_plus\x18\x01 \x01(\r\x12\x0f\n\x07pin_min\x18\x02 \x01(\r\x12@\n\x0c\x63\x61n_protocol\x18\x03 \x01(\x0e\x32*.com.jifeline.OpenOBD.Protocol.CanProtocol\x12?\n\x0c\x63\x61n_bit_rate\x18\x04 \x01(\x0e\x32).com.jifeline.OpenOBD.Protocol.CanBitRate\x12I\n\x0btransceiver\x18\x05 \x01(\x0e\x32/.com.jifeline.OpenOBD.Protocol.TransceiverSpeedH\x00\x88\x01\x01\x42\x0e\n\x0c_transceiver\"\xa2\x01\n\x08KlineBus\x12\x0b\n\x03pin\x18\x01 \x01(\r\x12\x44\n\x0ekline_protocol\x18\x02 \x01(\x0e\x32,.com.jifeline.OpenOBD.Protocol.KlineProtocol\x12\x43\n\x0ekline_bit_rate\x18\x03 \x01(\x0e\x32+.com.jifeline.OpenOBD.Protocol.KlineBitRate\"\x18\n\tPlus15Bus\x12\x0b\n\x03pin\x18\x01 \x01(\r\"\t\n\x07\x44oipBus*q\n\x0b\x43\x61nProtocol\x12\x1a\n\x16\x43\x41N_PROTOCOL_UNDEFINED\x10\x00\x12\x16\n\x12\x43\x41N_PROTOCOL_ISOTP\x10\x01\x12\x15\n\x11\x43\x41N_PROTOCOL_TP20\x10\x02\x12\x17\n\x13\x43\x41N_PROTOCOL_FRAMES\x10\x03*\xad\x02\n\nCanBitRate\x12\x1a\n\x16\x43\x41N_BIT_RATE_UNDEFINED\x10\x00\x12\x15\n\x11\x43\x41N_BIT_RATE_1000\x10\x01\x12\x14\n\x10\x43\x41N_BIT_RATE_500\x10\x02\x12\x14\n\x10\x43\x41N_BIT_RATE_250\x10\x03\x12\x14\n\x10\x43\x41N_BIT_RATE_125\x10\x04\x12\x14\n\x10\x43\x41N_BIT_RATE_100\x10\x05\x12\x13\n\x0f\x43\x41N_BIT_RATE_94\x10\x06\x12\x15\n\x11\x43\x41N_BIT_RATE_83_3\x10\x07\x12\x13\n\x0f\x43\x41N_BIT_RATE_50\x10\x08\x12\x15\n\x11\x43\x41N_BIT_RATE_33_3\x10\t\x12\x13\n\x0f\x43\x41N_BIT_RATE_20\x10\n\x12\x13\n\x0f\x43\x41N_BIT_RATE_10\x10\x0b\x12\x12\n\x0e\x43\x41N_BIT_RATE_5\x10\x0c*j\n\x10TransceiverSpeed\x12\x1f\n\x1bTRANSCEIVER_SPEED_UNDEFINED\x10\x00\x12\x1a\n\x16TRANSCEIVER_SPEED_HIGH\x10\x01\x12\x19\n\x15TRANSCEIVER_SPEED_LOW\x10\x02*\x99\x02\n\rKlineProtocol\x12\x1c\n\x18KLINE_PROTOCOL_UNDEFINED\x10\x00\x12 \n\x1bKLINE_PROTOCOL_GENERIC_SLOW\x10\xe8\x07\x12 \n\x1bKLINE_PROTOCOL_GENERIC_FAST\x10\xe9\x07\x12\x1f\n\x1aKLINE_PROTOCOL_KWP841_SLOW\x10\xea\x07\x12!\n\x1cKLINE_PROTOCOL_ISO14230_SLOW\x10\xeb\x07\x12!\n\x1cKLINE_PROTOCOL_ISO14230_FAST\x10\xec\x07\x12\x1f\n\x1aKLINE_PROTOCOL_KWP760_SLOW\x10\xed\x07\x12\x1e\n\x19KLINE_PROTOCOL_HONDA_FAST\x10\xee\x07*y\n\x0cKlineBitRate\x12\x1c\n\x18KLINE_BIT_RATE_UNDEFINED\x10\x00\x12\x17\n\x13KLINE_BIT_RATE_9600\x10\x07\x12\x18\n\x14KLINE_BIT_RATE_10400\x10\x0b\x12\x18\n\x14KLINE_BIT_RATE_15625\x10\x12*Y\n\x06\x45ntity\x12\x14\n\x10\x45NTITY_UNDEFINED\x10\x00\x12\x10\n\x0c\x45NTITY_LOCAL\x10\x01\x12\x11\n\rENTITY_REMOTE\x10\x03\x12\x14\n\x10\x45NTITY_BROADCAST\x10\x04\x42\x02P\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'openobd_protocol.BusConfiguration_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'P\001'
  _globals['_CANPROTOCOL']._serialized_start=840
  _globals['_CANPROTOCOL']._serialized_end=953
  _globals['_CANBITRATE']._serialized_start=956
  _globals['_CANBITRATE']._serialized_end=1257
  _globals['_TRANSCEIVERSPEED']._serialized_start=1259
  _globals['_TRANSCEIVERSPEED']._serialized_end=1365
  _globals['_KLINEPROTOCOL']._serialized_start=1368
  _globals['_KLINEPROTOCOL']._serialized_end=1649
  _globals['_KLINEBITRATE']._serialized_start=1651
  _globals['_KLINEBITRATE']._serialized_end=1772
  _globals['_ENTITY']._serialized_start=1774
  _globals['_ENTITY']._serialized_end=1863
  _globals['_BUSCONFIGURATION']._serialized_start=75
  _globals['_BUSCONFIGURATION']._serialized_end=368
  _globals['_CANBUS']._serialized_start=371
  _globals['_CANBUS']._serialized_end=636
  _globals['_KLINEBUS']._serialized_start=639
  _globals['_KLINEBUS']._serialized_end=801
  _globals['_PLUS15BUS']._serialized_start=803
  _globals['_PLUS15BUS']._serialized_end=827
  _globals['_DOIPBUS']._serialized_start=829
  _globals['_DOIPBUS']._serialized_end=838
# @@protoc_insertion_point(module_scope)
