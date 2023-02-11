import random

from GeneratorJmen.Data.Name.names_gk import *
from GeneratorJmen.Data.Name.names_fi import *
from GeneratorJmen.Data.Name.names_pl import *
from GeneratorJmen.Data.Name.names_it import *
from GeneratorJmen.Data.Name.names_no import *
from GeneratorJmen.Data.Name.names_ne import *
from GeneratorJmen.Data.Name.names_se import *
from GeneratorJmen.Data.Name.names_hu import *
from GeneratorJmen.Data.Name.names_us import *
from GeneratorJmen.Data.Name.names_sk import *
from GeneratorJmen.Data.Name.names_fr import *
from GeneratorJmen.Data.Name.names_es import *
from GeneratorJmen.Data.Name.names_vn import *
from GeneratorJmen.Data.Name.names_au_aboriginal import *

from GeneratorJmen.Data.Name.Mans.mnames_cz import *
from GeneratorJmen.Data.Name.Womans.wnames_cz import *
from GeneratorJmen.Data.Name.Mans.mnames_gb_scotish import *
from GeneratorJmen.Data.Name.Womans.wnames_gb_scotish import *
from GeneratorJmen.Data.Name.Mans.mnames_au_aboriginal import *
from GeneratorJmen.Data.Name.Womans.wnames_au_aboriginal import *


intent_names_cz = (
    intent_mnames_cz,
    intent_wnames_cz,

)

intent_names_gb_scotish = (
    intent_wnames_gb_scotish,
    intent_wnames_gb_scotish,
)

intent_names_au_aboriginal=(
    intent_wnames_au_aboriginal,
    intent_mnames_au_aboriginal,
    intent_names_au_aboriginal,                 # jmena pro obe pohlavi
)

names_all = (
    intent_names_gk,
    intent_names_fi,
    intent_names_pl,
    intent_names_it,
    intent_names_no,
    intent_names_ne,
    intent_names_se,
    intent_names_hu,
    intent_names_us,
    intent_names_sk,
    intent_names_fr,
    intent_names_es,
    intent_names_vn,
    intent_names_cz,
    intent_names_gb_scotish,
    intent_names_au_aboriginal,
)


class Name:
    @staticmethod
    def get_random_tribe_name():
        return get_random_name()


@staticmethod
def get_random_name():
    return random.choice(random.choice(names_all))
