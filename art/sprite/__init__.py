
from python.xml.tags import Tag, Name, tags

def configure_sprite(
    mount = None,
    mount_head = 'mouse',
    mount_eyes = 'beady',
    mount_expression = 'normal',
    mount_goggles = False,
    mount_ears = 'mouse',
    mount_teeth = None,
    mount_horns = None,
    mount_legs = 'mouse',
    mount_tail = 'rat',
    mount_spots = False,
    mount_mane = False,
    mount_wings = None,
    mount_collar = False,
    mount_bow_tie = False,
    dinosaur_ventral_blades = False,
    rider = False,
    rider_face = 'round',
    rider_ears = 'human',
    rider_eyes = 'normal',
    rider_mouth = None,
    rider_hair = 'short',
    rider_hair_bangs = True,
    rider_shirt = True,
    rider_shoes = True,
    rider_pants = True,
    rider_breastplate = True,
    rider_hand_left_holds = None,
    rider_hand_right_holds = None,
    rider_shoulder_left_buckler = False,
    rider_shoulder_left_sword = False,
    rider_shoulder_right_buckler = False,
    rider_shoulder_right_sword = False,
    saddle = False,
):

    mount_body = mount
    rodent = mount and mount_head in ('mouse', 'otter', 'elephant', 'bear')
    dinosaur = mount and mount_head == 'dinosaur'

    # head
    rodent_head_mouse = (rodent and mount_head == 'mouse')
    rodent_head_otter = (rodent and mount_head == 'otter')
    rodent_head_elephant = (rodent and mount_head == 'elephant')
    rodent_head_bear = (rodent and mount_head == 'bear')
    dinosaur_head = dinosaur

    # eyes
    rodent_eyes_beady = rodent and (mount_eyes == 'beady')
    rodent_eyes_wombat = rodent and (mount_eyes == 'wombat')
    rodent_eyes_elephant = rodent and (mount_eyes == 'elephant')

    dinosaur_eyes_normal = dinosaur and (mount_expression == 'normal')
    dinosaur_eyes_evil = dinosaur and (mount_expression == 'evil')

    # ears
    rodent_ear_mouse_left = \
    rodent_ear_mouse_right = \
        (rodent and mount_ears == 'mouse')
    rodent_ear_bunny_left = \
    rodent_ear_bunny_right = \
        (rodent and mount_ears == 'bunny')
    rodent_ear_elephant_left = \
    rodent_ear_elephant_right = \
        (rodent and mount_ears == 'elephant')
    rodent_ear_wolf_left = \
    rodent_ear_wolf_right = \
        (rodent and mount_ears == 'wolf')
    rodent_ear_poodle_left = \
        (rodent and mount_ears == 'poodle')
    dinosaur_ear_bunny_left = \
    dinosaur_ear_bunny_right = \
        (dinosaur and mount_ears == 'bunny')

    # goggles
    rodent_goggles = rodent and mount_goggles
    dinosaur_goggles = dinosaur and mount_goggles

    # legs
    mount_arm_bunny_left = \
    mount_arm_bunny_right = \
    mount_leg_bunny_left = \
    mount_leg_bunny_right = \
        mount and (mount_legs == 'bunny')
    mount_arm_chicken_left = \
    mount_arm_chicken_right = \
    mount_leg_chicken_left = \
    mount_leg_chicken_right = \
        mount and (mount_legs == 'chicken')
    mount_arm_elephant_left = \
    mount_arm_elephant_right = \
    mount_leg_elephant_left = \
    mount_leg_elephant_right = \
        mount and (mount_legs == 'elephant')
    mount_arm_mouse_left = \
    mount_arm_mouse_right =  \
    mount_leg_mouse_left = \
    mount_leg_mouse_right = \
        mount and (mount_legs == 'mouse')
    mount_arm_wombat_left = \
    mount_arm_wombat_right =  \
    mount_leg_wombat_left = \
    mount_leg_wombat_right = \
        mount and (mount_legs == 'wombat')

    # tail
    mount_tail_badger = mount and (mount_tail == 'badger')
    mount_tail_bunny = mount and (mount_tail == 'bunny')
    mount_tail_curly = mount and (mount_tail == 'curly')
    mount_tail_otter = mount and (mount_tail == 'otter')
    mount_tail_rat = mount and (mount_tail == 'rat')

    # wings
    mount_wing_bat_left = \
    mount_wing_bat_right = \
        (mount and mount_wings == 'bat')
    mount_wing_bird_left = \
    mount_wing_bird_right = \
        (mount and mount_wings == 'bird')
    mount_wing_hummingbird_left = \
    mount_wing_hummingbird_right = \
        (mount and mount_wings == 'hummingbird')

    # features
    mount_mane = mount and mount_mane

    # teeth
    rodent_fangs = rodent and (mount_teeth == 'fangs')
    rodent_teeth_buck = (
        rodent and
        (mount_teeth == 'buck') and
        mount_head in ('mouse', 'otter')
    )
    rodent_tusks_elephant = rodent and (mount_teeth == 'elephant') and rodent_head_elephant
    rodent_tusk_mastadon_left = \
    rodent_tusk_mastadon_right = \
        rodent and (mount_teeth == 'mastadon') and rodent_head_elephant
    dinosaur_fangs = dinosaur and (mount_teeth == 'fangs')
    dinosaur_teeth_buck = dinosaur and (mount_teeth == 'buck')

    # horn
    rodent_antler_left = rodent_antler_right = rodent and (mount_horns == 'moose')
    rodent_horn_rhino = rodent and (mount_horns == 'rhino')
    rodent_unihorn = rodent and (mount_horns == 'unicorn')
    dinosaur_horn = dinosaur and (mount_horns == 'spike')

    # ventral blades
    dinosaur_ventral_blades_front = \
    dinosaur_ventral_blades_back = \
        dinosaur and dinosaur_ventral_blades

    rodent_nostril = (
        rodent and
        (
            rodent_head_mouse or
            rodent_head_otter 
        ) and
        not rodent_horn_rhino
    )
    rodent_snout = (
        rodent and
        rodent_head_bear and
        not rodent_horn_rhino
    )

    mount_spots_cow = \
    mount_spots_rump = \
        mount and mount_spots

    # accessories
    dinosaur_collar = dinosaur and mount_collar
    dinosaur_bow_tie = dinosaur_collar and mount_bow_tie

    # rider
    rider_eyes_pupils = \
    rider_body_male = \
    rider_body_male_fuzz = \
    rider_hand_left = \
    rider_hand_left_thumb = \
    rider_hand_right = \
    rider_hand_right_thumb = \
    rider_leg_left = \
    rider_leg_right = \
    rider_torso = \
    rider_arm_left = \
    rider_arm_right = \
    rider_fuzz = \
        rider

    # eyes
    rider_eyes_normal = rider and (rider_eyes == 'normal')
    rider_eyes_aggressive = rider and (rider_eyes == 'aggressive')
    rider_eyes_surprised = rider and (rider_eyes == 'surprised')

    # mouth
    rider_smile = rider and (rider_mouth == 'smile')
    rider_grimmace = rider and (rider_mouth == 'grimmace')

    # ears
    rider_ear_elven_left = \
    rider_ear_elven_right = \
        rider and (rider_ears == 'elven')
    rider_ear_round_left = \
    rider_ear_round_right = \
        rider and (rider_ears == 'human')

    # face
    rider_face_long = \
    rider_face_long_shadow = \
        rider and (rider_face == 'long')
    rider_face_round = \
    rider_face_round_shadow = \
        rider and (rider_face == 'round')

    # hair
    rider_hair_long = rider and (rider_hair == 'long')
    rider_hair_short = rider and (rider_hair == 'short')
    rider_hair_bangs = (
        rider and
        rider_hair in ('long', 'short') and
        rider_hair_bangs
    )

    # left hand
    rider_hand_left_buckler = rider and (rider_hand_left_holds == 'buckler')
    rider_hand_left_knife = rider and (rider_hand_left_holds == 'knife')
    rider_hand_left_sword = rider and (rider_hand_left_holds == 'sword')

    # right hand
    rider_hand_right_buckler = rider and (rider_hand_right_holds == 'buckler')
    rider_hand_right_knife = rider and (rider_hand_right_holds == 'knife')
    rider_hand_right_sword = rider and (rider_hand_right_holds == 'sword')

    # left shoulder
    rider_shoulder_left_buckler = rider and rider_shoulder_left_buckler
    rider_shoulder_left_sword = rider and rider_shoulder_left_sword

    # right shoulder
    rider_shoulder_right_buckler = rider and rider_shoulder_right_buckler
    rider_shoulder_right_sword = rider and rider_shoulder_right_sword

    # shirt
    rider_shirt = rider and rider_shirt

    # pants
    rider_pant_small_left = \
    rider_pant_small_right = \
        rider and rider_pants

    # shoes
    rider_shoe_left = \
    rider_shoe_right = \
        rider and rider_shoes

    rider_breastplate = \
    rider_breastplate_shine = \
        rider and rider_breastplate

    # saddle
    saddle_front = saddle_left = saddle_right = mount and saddle

    return set(
        key
        for key, value in vars().items()
        if value == True
    )

class SpriteRequest(HTTPRequest):
    def process(self):

        image = self.service.image

        configuration = configure_sprite(
            mount = self.args.has_key('mount'),
            mount_head = self.args.has_key('mount_head') and self.args['mount_head'][0],
            mount_eyes = self.args.has_key('mount_eyes') and self.args['mount_eyes'][0],
            mount_expression = self.args.has_key('mount_expression') and self.args['mount_expression'][0],
            mount_goggles = self.args.has_key('mount_goggles'),
            mount_wings = self.args.has_key('mount_wings') and self.args['mount_wings'][0],
            mount_horns = self.args.has_key('mount_horns') and self.args['mount_horns'][0],
            mount_legs = self.args.has_key('mount_legs') and self.args['mount_legs'][0],
            mount_tail = self.args.has_key('mount_tail') and self.args['mount_tail'][0],
            mount_teeth = self.args.has_key('mount_teeth') and self.args['mount_teeth'][0],
            mount_spots = self.args.has_key('mount_spots'),
            mount_mane = self.args.has_key('mount_mane'),
            mount_ears = self.args.has_key('mount_ears') and self.args['mount_ears'][0],
            mount_collar = self.args.has_key('mount_collar'),
            mount_bow_tie = self.args.has_key('mount_bow_tie'),
            dinosaur_ventral_blades = self.args.has_key('dinosaur_ventral_blades'),
            rider = self.args.has_key('rider'),
            rider_face = self.args.has_key('rider_face') and self.args['rider_face'][0],
            rider_ears = self.args.has_key('rider_ears') and self.args['rider_ears'][0],
            rider_eyes = self.args.has_key('rider_eyes') and self.args['rider_eyes'][0],
            rider_hair = self.args.has_key('rider_hair') and self.args['rider_hair'][0],
            rider_hair_bangs = self.args.has_key('rider_hair_bangs'),
            rider_shirt = self.args.has_key('rider_shirt'),
            rider_shoes = self.args.has_key('rider_shoes'),
            rider_pants = self.args.has_key('rider_pants'),
            rider_breastplate = self.args.has_key('rider_breastplate'),
            rider_hand_left_holds = self.args.has_key('rider_hand_left_holds') and self.args['rider_hand_left_holds'][0],
            rider_hand_right_holds = self.args.has_key('rider_hand_right_holds') and self.args['rider_hand_right_holds'][0],
            rider_shoulder_left_buckler = self.args.has_key('rider_shoulder_left_buckler'),
            rider_shoulder_left_sword = self.args.has_key('rider_shoulder_left_sword'),
            rider_shoulder_right_buckler = self.args.has_key('rider_shoulder_right_buckler'),
            rider_shoulder_right_sword = self.args.has_key('rider_shoulder_right_sword'),
            saddle = self.args.has_key('saddle'),
        )

        self.setResponseCode(200)
        self.setHeader('Content-type', 'image/svg+xml')

        self.write(
            str(tags.svg(
                image.attributes,
                image[Name('defs')],
                (
                    tag
                    for tag in image
                    if isinstance(tag, Tag) and
                    'inkscape:label' in tag and
                    tag['inkscape:label'] in configuration
                )
            ).xml)
        )

        self.finish()

class SpriteService(object):
    def __init__(self, file_name):
        self.image = Tag.parse(file_name)

