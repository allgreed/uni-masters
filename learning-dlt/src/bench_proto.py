import os
import binascii
import random
import time
import src.json_proto as JSONProtocol
import src.bin_proto as BinaryProtocol

import pandas as pd


def randhex(count):
    assert count % 2 == 0
    return binascii.b2a_hex(os.urandom(count // 2))


def generate_example():
    trns = []
    for _ in range(random.randint(1, 15)):
        trns.append({"from_ac": randhex(128), "to_ac": randhex(128)})

    return {"block": {"hash": randhex(64),
            "hashedContent": {
                "nonce": random.randint(0, 2 ** 31), "prev_hash": randhex(64), "timestamp": random.randint(0, 2 ** 31), "transactions": trns}}}


EXAMPLES = []

for i in range(100):
    EXAMPLES.append(generate_example())


RESULTS = []
DATA = [(0, 'src.bin_proto', 0.0006177425384521484, 1105), (1, 'src.bin_proto', 0.000713348388671875, 1873), (2, 'src.bin_proto', 0.0003447532653808594, 849), (3, 'src.bin_proto', 0.0003447532653808594, 721), (4, 'src.bin_proto', 0.0002598762512207031, 593), (5, 'src.bin_proto', 0.0006530284881591797, 1617), (6, 'src.bin_proto', 0.0006403923034667969, 1489), (7, 'src.bin_proto', 0.0007445812225341797, 1745), (8, 'src.bin_proto', 0.0005364418029785156, 1361), (9, 'src.bin_proto', 0.0003457069396972656, 849), (10, 'src.bin_proto', 0.0005438327789306641, 1489), (11, 'src.bin_proto', 0.0006463527679443359, 1745), (12, 'src.bin_proto', 0.00026226043701171875, 593), (13, 'src.bin_proto', 0.0003135204315185547, 721), (14, 'src.bin_proto', 0.0007491111755371094, 1617), (15, 'src.bin_proto', 0.0006122589111328125, 1617), (16, 'src.bin_proto', 0.0005571842193603516, 1489), (17, 'src.bin_proto', 0.00034356117248535156, 849), (18, 'src.bin_proto', 0.0006716251373291016, 1617), (19, 'src.bin_proto', 0.00020432472229003906, 337), (20, 'src.bin_proto', 0.0004634857177734375, 1233), (21, 'src.bin_proto', 0.0006093978881835938, 1361), (22, 'src.bin_proto', 0.0004956722259521484, 1233), (23, 'src.bin_proto', 0.00024962425231933594, 465), (24, 'src.bin_proto', 0.0008075237274169922, 2001), (25, 'src.bin_proto', 0.0003764629364013672, 849), (26, 'src.bin_proto', 0.0006561279296875, 1489), (27, 'src.bin_proto', 0.0004909038543701172, 721), (28, 'src.bin_proto', 0.0005304813385009766, 1361), (29, 'src.bin_proto', 0.0001811981201171875, 337), (30, 'src.bin_proto', 0.00043773651123046875, 1105), (31, 'src.bin_proto', 0.00020194053649902344, 209), (32, 'src.bin_proto', 0.0004467964172363281, 1105), (33, 'src.bin_proto', 0.00033974647521972656, 849), (34, 'src.bin_proto', 0.0002567768096923828, 593), (35, 'src.bin_proto', 0.0005412101745605469, 1489), (36, 'src.bin_proto', 0.0006668567657470703, 1873), (37, 'src.bin_proto', 0.00021910667419433594, 465), (38, 'src.bin_proto', 0.0006842613220214844, 1873), (39, 'src.bin_proto', 0.0004222393035888672, 1105), (40, 'src.bin_proto', 0.0005955696105957031, 1617), (41, 'src.bin_proto', 0.00018072128295898438, 337), (42, 'src.bin_proto', 0.0005757808685302734, 1617), (43, 'src.bin_proto', 0.0002484321594238281, 465), (44, 'src.bin_proto', 0.0008127689361572266, 1489), (45, 'src.bin_proto', 0.0006182193756103516, 1617), (46, 'src.bin_proto', 0.0005803108215332031, 1617), (47, 'src.bin_proto', 0.0007028579711914062, 2001), (48, 'src.bin_proto', 0.00030350685119628906, 721), (49, 'src.bin_proto', 0.0001354217529296875, 209), (50, 'src.bin_proto', 0.0004875659942626953, 1361), (51, 'src.bin_proto', 0.0002148151397705078, 465), (52, 'src.bin_proto', 0.0003898143768310547, 721), (53, 'src.bin_proto', 0.0004425048828125, 1105), (54, 'src.bin_proto', 0.0006623268127441406, 1617), (55, 'src.bin_proto', 0.00046324729919433594, 1105), (56, 'src.bin_proto', 0.00034880638122558594, 465), (57, 'src.bin_proto', 0.0007228851318359375, 1617), (58, 'src.bin_proto', 0.0006225109100341797, 1617), (59, 'src.bin_proto', 0.0005891323089599609, 1489), (60, 'src.bin_proto', 0.00018930435180664062, 337), (61, 'src.bin_proto', 0.0008041858673095703, 1873), (62, 'src.bin_proto', 0.0006520748138427734, 1873), (63, 'src.bin_proto', 0.0008635520935058594, 1617), (64, 'src.bin_proto', 0.0007147789001464844, 1873), (65, 'src.bin_proto', 0.0003559589385986328, 209), (66, 'src.bin_proto', 0.00034999847412109375, 721), (67, 'src.bin_proto', 0.00028133392333984375, 593), (68, 'src.bin_proto', 0.0006132125854492188, 1617), (69, 'src.bin_proto', 0.0006072521209716797, 1617), (70, 'src.bin_proto', 0.0006959438323974609, 1873), (71, 'src.bin_proto', 0.00039386749267578125, 977), (72, 'src.bin_proto', 0.0002727508544921875, 593), (73, 'src.bin_proto', 0.00030803680419921875, 721), (74, 'src.bin_proto', 0.00030922889709472656, 721), (75, 'src.bin_proto', 0.0006277561187744141, 1745), (76, 'src.bin_proto', 0.0003724098205566406, 977), (77, 'src.bin_proto', 0.00025081634521484375, 593), (78, 'src.bin_proto', 0.0006279945373535156, 1617), (79, 'src.bin_proto', 0.00022649765014648438, 465), (80, 'src.bin_proto', 0.0005795955657958984, 1617), (81, 'src.bin_proto', 0.0003323554992675781, 849), (82, 'src.bin_proto', 0.0003764629364013672, 977), (83, 'src.bin_proto', 0.0004177093505859375, 1105), (84, 'src.bin_proto', 0.0004527568817138672, 1233), (85, 'src.bin_proto', 0.00018167495727539062, 337), (86, 'src.bin_proto', 0.0005290508270263672, 1489), (87, 'src.bin_proto', 0.0007030963897705078, 2001), (88, 'src.bin_proto', 0.00017690658569335938, 337), (89, 'src.bin_proto', 0.00025153160095214844, 593), (90, 'src.bin_proto', 0.00029468536376953125, 721), (91, 'src.bin_proto', 0.0007715225219726562, 1873), (92, 'src.bin_proto', 0.00014495849609375, 209), (93, 'src.bin_proto', 0.000274658203125, 465), (94, 'src.bin_proto', 0.00036144256591796875, 849), (95, 'src.bin_proto', 0.0005352497100830078, 1361), (96, 'src.bin_proto', 0.0007798671722412109, 2001), (97, 'src.bin_proto', 0.0007252693176269531, 2001), (98, 'src.bin_proto', 0.0003590583801269531, 849), (99, 'src.bin_proto', 0.0009007453918457031, 1873), (0, 'src.json_proto', 0.0007479190826416016, 2543), (1, 'src.json_proto', 0.0008537769317626953, 4259), (2, 'src.json_proto', 0.0004410743713378906, 1971), (3, 'src.json_proto', 0.0003974437713623047, 1685), (4, 'src.json_proto', 0.0003390312194824219, 1399), (5, 'src.json_proto', 0.0007269382476806641, 3686), (6, 'src.json_proto', 0.0006890296936035156, 3401), (7, 'src.json_proto', 0.0008323192596435547, 3974), (8, 'src.json_proto', 0.0006866455078125, 3115), (9, 'src.json_proto', 0.0005612373352050781, 1971), (10, 'src.json_proto', 0.0006756782531738281, 3401), (11, 'src.json_proto', 0.0007734298706054688, 3973), (12, 'src.json_proto', 0.00034809112548828125, 1399), (13, 'src.json_proto', 0.0003886222839355469, 1685), (14, 'src.json_proto', 0.0007638931274414062, 3687), (15, 'src.json_proto', 0.0007188320159912109, 3688), (16, 'src.json_proto', 0.00067901611328125, 3402), (17, 'src.json_proto', 0.00045490264892578125, 1972), (18, 'src.json_proto', 0.0007245540618896484, 3688), (19, 'src.json_proto', 0.00025153160095214844, 828), (20, 'src.json_proto', 0.0007464885711669922, 2830), (21, 'src.json_proto', 0.0006778240203857422, 3115), (22, 'src.json_proto', 0.0006368160247802734, 2830), (23, 'src.json_proto', 0.00031638145446777344, 1114), (24, 'src.json_proto', 0.0010192394256591797, 4545), (25, 'src.json_proto', 0.0004677772521972656, 1971), (26, 'src.json_proto', 0.0009922981262207031, 3402), (27, 'src.json_proto', 0.0004818439483642578, 1685), (28, 'src.json_proto', 0.0007381439208984375, 3115), (29, 'src.json_proto', 0.0002696514129638672, 827), (30, 'src.json_proto', 0.0005669593811035156, 2544), (31, 'src.json_proto', 0.00023984909057617188, 541), (32, 'src.json_proto', 0.0005462169647216797, 2543), (33, 'src.json_proto', 0.0007491111755371094, 1971), (34, 'src.json_proto', 0.0005040168762207031, 1400), (35, 'src.json_proto', 0.0006909370422363281, 3401), (36, 'src.json_proto', 0.0008192062377929688, 4258), (37, 'src.json_proto', 0.0002930164337158203, 1113), (38, 'src.json_proto', 0.0008275508880615234, 4258), (39, 'src.json_proto', 0.0005471706390380859, 2542), (40, 'src.json_proto', 0.0007212162017822266, 3686), (41, 'src.json_proto', 0.0002498626708984375, 827), (42, 'src.json_proto', 0.0007765293121337891, 3688), (43, 'src.json_proto', 0.00029850006103515625, 1111), (44, 'src.json_proto', 0.000797271728515625, 3401), (45, 'src.json_proto', 0.000728607177734375, 3686), (46, 'src.json_proto', 0.0008461475372314453, 3687), (47, 'src.json_proto', 0.001018524169921875, 4545), (48, 'src.json_proto', 0.0004305839538574219, 1686), (49, 'src.json_proto', 0.000209808349609375, 542), (50, 'src.json_proto', 0.0007076263427734375, 3114), (51, 'src.json_proto', 0.0003807544708251953, 1112), (52, 'src.json_proto', 0.0004055500030517578, 1685), (53, 'src.json_proto', 0.0005652904510498047, 2543), (54, 'src.json_proto', 0.0008680820465087891, 3688), (55, 'src.json_proto', 0.0007154941558837891, 2543), (56, 'src.json_proto', 0.0003323554992675781, 1113), (57, 'src.json_proto', 0.0007274150848388672, 3688), (58, 'src.json_proto', 0.0007252693176269531, 3686), (59, 'src.json_proto', 0.0006701946258544922, 3402), (60, 'src.json_proto', 0.0002434253692626953, 827), (61, 'src.json_proto', 0.0009205341339111328, 4258), (62, 'src.json_proto', 0.0008115768432617188, 4260), (63, 'src.json_proto', 0.0007176399230957031, 3688), (64, 'src.json_proto', 0.0008058547973632812, 4259), (65, 'src.json_proto', 0.0002040863037109375, 541), (66, 'src.json_proto', 0.0003821849822998047, 1685), (67, 'src.json_proto', 0.0003333091735839844, 1397), (68, 'src.json_proto', 0.000751495361328125, 3687), (69, 'src.json_proto', 0.00074005126953125, 3688), (70, 'src.json_proto', 0.0008108615875244141, 4259), (71, 'src.json_proto', 0.0004787445068359375, 2258), (72, 'src.json_proto', 0.00033593177795410156, 1399), (73, 'src.json_proto', 0.0003876686096191406, 1683), (74, 'src.json_proto', 0.00037980079650878906, 1686), (75, 'src.json_proto', 0.0008285045623779297, 3972), (76, 'src.json_proto', 0.0006489753723144531, 2257), (77, 'src.json_proto', 0.0003619194030761719, 1399), (78, 'src.json_proto', 0.0007960796356201172, 3687), (79, 'src.json_proto', 0.00029778480529785156, 1112), (80, 'src.json_proto', 0.0008056163787841797, 3687), (81, 'src.json_proto', 0.00046181678771972656, 1971), (82, 'src.json_proto', 0.0005567073822021484, 2258), (83, 'src.json_proto', 0.0007498264312744141, 2543), (84, 'src.json_proto', 0.0006256103515625, 2829), (85, 'src.json_proto', 0.00026702880859375, 828), (86, 'src.json_proto', 0.0007314682006835938, 3401), (87, 'src.json_proto', 0.0008907318115234375, 4544), (88, 'src.json_proto', 0.00024509429931640625, 826), (89, 'src.json_proto', 0.0003409385681152344, 1399), (90, 'src.json_proto', 0.00037980079650878906, 1685), (91, 'src.json_proto', 0.0008058547973632812, 4259), (92, 'src.json_proto', 0.0001964569091796875, 542), (93, 'src.json_proto', 0.0002868175506591797, 1111), (94, 'src.json_proto', 0.0004489421844482422, 1971), (95, 'src.json_proto', 0.0006260871887207031, 3115), (96, 'src.json_proto', 0.0008671283721923828, 4545), (97, 'src.json_proto', 0.0009889602661132812, 4545), (98, 'src.json_proto', 0.00046896934509277344, 1972), (99, 'src.json_proto', 0.0008099079132080078, 4259)]

def run():
    # for proto in (BinaryProtocol, JSONProtocol):
    #   # for i, ex in enumerate(EXAMPLES):
    #       # start = time.time()
    #       # msg = proto.NewBlock.from_parse(**ex)
    #       # transit_msg = proto.encode(msg)
    #       # proto.decode(transit_msg)
    #       # end = time.time()

    #       # total = end - start
    #       # size = len(transit_msg)

    #       # RESULTS.append((i, proto.__name__, total, size))
    # print(RESULTS)

    # print(DATA)
    df = pd.DataFrame(DATA)
    print(df)

    df_json = df[df[1] == 'src.json_proto']
    print(df_json)
    df_bin = df[df[1] == 'src.bin_proto']
    print(df_bin)

    print("json size", df_json[3].mean(), df_json[3].std())
    print("bin size ", df_bin[3].mean(), df_bin[3].std())

    print("json time", df_json[2].mean() * 1000, df_json[2].std() * 1000)
    print("bin time ", df_bin[2].mean() * 1000, df_bin[2].std() * 1000)


if __name__ == "__main__":
    run()
