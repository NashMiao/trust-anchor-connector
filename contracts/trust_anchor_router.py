from ontology.builtins import concat, append
from ontology.interop.System.Storage import GetContext, Put, Get, Delete
from ontology.interop.Ontology.Runtime import CheckWitness, Base58ToAddress
from ontology.interop.System.Runtime import CheckWitness, Deserialize, Serialize

TA_LIST_KEY = 'TALIST'

ctx = GetContext()
admin = Base58ToAddress('ANDfjwrUroaVtvBguDtrWKRMyxFwvVwnZD')


def main(operation, args):
    if operation == 'register_trust_anchor':
        return register_trust_anchor(args[0], args[1])
    elif operation == 'get_trust_anchor_list':
        return get_trust_anchor_list()
    else:
        revert()


def register_trust_anchor(ta_name, ont_id):
    require_witness(admin)
    ta_key = concat('TA', ta_name)
    require_not_exist(ta_key)
    serialize_ta_list = Get(ctx, TA_LIST_KEY)
    if serialize_ta_list is None:
        ta_list = []
    else:
        ta_list = Deserialize(serialize_ta_list)
    ta_list.append(ta_name)
    serialize_ta_list = Serialize(ta_list)
    Put(ctx, TA_LIST_KEY, serialize_ta_list)
    Put(ctx, ta_key, ont_id)


def get_trust_anchor_list():
    serialize_ta_list = Get(ctx, TA_LIST_KEY)
    if serialize_ta_list is None:
        serialize_ta_list = Serialize([])
    return serialize_ta_list


def revert():
    """
    Revert the transaction. The opcodes of this function is `09f7f6f5f4f3f2f1f000f0`,
    but it will be changed to `ffffffffffffffffffffff` since opcode THROW doesn't
    work, so, revert by calling unused opcode.
    """
    raise Exception(0xF1F1F2F2F3F3F4F4)


def require(condition):
    if not condition:
        revert()


def require_witness(witness):
    require(CheckWitness(witness))


def require_not_exist(ctx_key):
    if Get(ctx, ctx_key):
        revert()
