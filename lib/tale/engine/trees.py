
from things import Thing
from plants import Plant, Deciduous
from fruit import *
from flowers import *
from cones import *
from nuts import *

class Lumber(Thing):
    pass

class Tree(Plant):
    collective = 'grove' #, 'glade', 'forest'
    lumber = Lumber

class Evergreen(Tree):
    pass

class FlowerTree(Tree):
    flower = Flower

class FruitTree(FlowerTree):
    fruit = Fruit

class BerryTree(FruitTree):
    berry = Berry

class NutTree(FlowerTree):
    nut = Nut

class Conifer(Evergreen):
    # soft wood
    cone = Cone

class HardwoodTree(Tree):
    pass

class Cypress(Conifer):
    pass

class Juniper(Cypress):
    pass

class Redwood(Cypress):
    pass

class PineFamilyTree(Conifer):
    cone = PineCone

class Pine(PineFamilyTree):
    pass

class Spruce(PineFamilyTree):
    pass

class Spruce(PineFamilyTree):
    pass

class Larch(PineFamilyTree):
    pass

class Fir(PineFamilyTree):
    pass

class Cedar(PineFamilyTree):
    pass

class Yew(Conifer):
    pass

class Ginkgo(Tree):
    pass

class Cycad(Tree):
    cone = Cone

class FernTree(Tree):
    pass

class BirchFamilyTree(HardwoodTree):
    pass

class Birch(BirchFamilyTree):
    pass

class Alder(BirchFamilyTree):
    pass

class Cactus(FlowerTree):
    flower = Flower

class Saguaro(Cactus):
    pass

class PersimmonTree(FruitTree):
    fruit = Persimmon

class HazelTree(NutTree, BirchFamilyTree):
    nut = HazelNut

class MangoTree(FruitTree):
    fruit = Mango

class WalnutTree(NutTree):
    nut = Walnut

class Magnolia(FlowerTree):
    flower = Magnolia

class CashewTree(NutTree):
    nut = Cashew

class Holly(BerryTree):
    pass

class Beech(Deciduous):
    pass

class ChestnutTree(Beech):
    nut = Chestnut

class Oak(Beech, Conifer):
    pass

class Hickory(WalnutTree):
    pass

class Wingnut(WalnutTree):
    pass

class LaurelTree(HardwoodTree):
    pass

class CinnamonTree(LaurelTree):
    pass

class AvocadoTree(LaurelTree):
    pass

class MagnoliaTree(HardwoodTree):
    pass

class MallowTree(HardwoodTree):
    pass

class CacoaTree(MallowTree):
    pass

class BalsaTree(MallowTree):
    pass

class LindenTree(MallowTree):
    pass

class MahoganyTree(HardwoodTree):
    pass

class MyrtleTree(HardwoodTree):
    pass

class GuavaTree(FruitTree, MyrtleTree):
    fruit = Guava

class OliveTree(FruitTree, HardwoodTree):
    fruit = Olive

class AshTree(OliveTree):
    pass

class RoseTree(HardwoodTree):
    pass

class Rowan(BerryTree, RoseTree):
    pass

class WhitebeamTree(BerryTree, RoseTree):
    pass

class Hawthorn(FruitTree, RoseTree):
    pass

class PearTree(FruitTree, RoseTree):
    fruit = Pear

class AppleTree(FruitTree, RoseTree):
    fruit = Apple

class AlmondTree(NutTree, RoseTree):
    nut = Almond

class CherryTree(RoseTree):
    fruit = Cherry

class PeachTree(RoseTree):
    fruit = Peach

class ApricotTree(RoseTree):
    fruit = Apricot

class PlumTree(RoseTree):
    fruit = Plum

class CoffeeTree(HardwoodTree):
    fruit = CoffeeBean

class RueTree(HardwoodTree):
    pass

class CorkTree(RueTree):
    pass

class WillowFamilyTree(HardwoodTree):
    pass

class WillowTree(WillowFamilyTree):
    pass

class Aspen(WillowFamilyTree):
    pass

class Poplar(WillowFamilyTree):
    pass

class SoapberryFamilyTree(HardwoodTree):
    pass

class Maple(SoapberryFamilyTree):
    pass

class Buckeye(SoapberryFamilyTree):
    pass

class CamelliaTree(HardwoodTree):
    pass

class Teak(HardwoodTree):
    plural = 'teak'

class Elm(HardwoodTree):
    pass

class JoshuaTree(Tree):
    pass

class PalmTree(Tree):
    pass

class CoconutTree(PalmTree):
    pass

class DateTree(PalmTree):
    pass

