import logging
import unittest

# 配置日志输出的格式
from util.TextFormatUtil import TextFormatUtil

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', level=logging.DEBUG)

csv_text_data = "Delivery Mode,Order ID,Order Date,Order Time,Pickup Date,Pickup Time,SKU ID ,Merchant Product ID,SKU Name (Chinese),Total Qty,SKU Name (English),Color (Chinese),Color (English),Size,status,Volume (m3),Waybill,Delivery Date,Is Shop Order?\nStandard Delivery,H240112056903,2024-01-12,20:32:13,2024-01-22,17:00:00,P0122001_S_77108-BKCC-9,77108-BKCC,\"SKECHERS - HOLDREDGE 男裝工作鞋 (多款尺碼可供選購)\",1,\"SKECHERS - HOLDREDGE MEN'S WORK SHOES (Multiple Sizes Available)\",黑色/炭灰色,Black/Charcoal,US 9,CONFIRMED,0.016848,6535945045,2024-01-23,No\nStandard Delivery,H240113042638,2024-01-13,23:37:03,2024-01-22,17:00:00,P0122001_S_403766L-WHT-2,403766L-WHT,\"SKECHERS - SELECTORS 兒童返學鞋 (多款尺碼可供選購)\",1,\"SKECHERS - SELECTORS KIDS' SCHOOL SHOES (Multiple Sizes Available)\",白色,White,US 2,CONFIRMED,0.016848,6537744788,2024-01-23,No\nStandard Delivery,H240113042638,2024-01-13,23:37:03,2024-01-22,17:00:00,P0122001_S_85715L-BBK-2,85715L-BBK,\"SKECHERS - BACK TO S 兒童返學鞋 (多款尺碼可供選購)\",1,\"SKECHERS - BACK TO S KIDS' SCHOOL SHOES (Multiple Sizes Available)\",黑色,Black,US 2,CONFIRMED,0.016848,6537744788,2024-01-23,No\nStandard Delivery,H240113042638,2024-01-13,23:37:03,2024-01-22,17:00:00,P0122001_S_403766L-WHT-1,403766L-WHT,\"SKECHERS - SELECTORS 兒童返學鞋 (多款尺碼可供選購)\",1,\"SKECHERS - SELECTORS KIDS' SCHOOL SHOES (Multiple Sizes Available)\",白色,White,US 1,CONFIRMED,0.016848,6537744788,2024-01-23,No\nStandard Delivery,H240117033472,2024-01-17,12:52:13,2024-01-22,17:00:00,P0122001_S_128075-GYLV-8,128075-GYLV,\"SKECHERS - GO RUN CONSISTENT 女裝跑步鞋 (多款尺碼可供選購)\",1,\"SKECHERS - GO RUN CONSISTENT WOMEN'S RUNNING SHOES (Multiple Sizes Available)\",灰白色/紫色,Grey/Purple,US 8,CONFIRMED,0.013104,6542854997,2024-01-23,Yes\nStandard Delivery,H240117050367,2024-01-17,15:14:04,2024-01-22,17:00:00,P0122001_S_149708-BBK-8,149708-BBK,\"SKECHERS - SLIP INS 速穿科技: ULTRA FLEX 3.0 女裝運動鞋 (多款尺碼可供選購)\",1,\"SKECHERS - SLIP INS: ULTRA FLEX 3.0 WOMEN'S SPORT SHOES (Multiple Sizes Available)\",黑色,Black,US 8,CONFIRMED,0.016848,6543123991,2024-01-23,No\nStandard Delivery,H240118057564,2024-01-18,20:20:32,2024-01-22,17:00:00,P0122001_S_88888250-WHT-7-5,88888250-WHT,\"SKECHERS - I-CONIK 女裝休閒鞋 (多款尺碼可供選購)\",1,\"SKECHERS - I-CONIK SPORT SHOES (Multiple Sizes Available)\",白色,White,US 7.5,CONFIRMED,0.013104,6545679692,2024-01-23,No\nStandard Delivery,H240119016291,2024-01-19,12:34:38,2024-01-22,17:00:00,P0122001_S_232625-WNVR-9,232625-WNVR,\"SKECHERS - VAPOR FOAM 男裝運動鞋 (多款尺碼可供選購)\",1,\"SKECHERS - VAPOR FOAM MEN'S SPORT SHOES (Multiple Sizes Available)\",白藍紅,White Blue Red,US 9,CONFIRMED,0.013104,6547085269,2024-01-23,No\nStandard Delivery,H240119035751,2024-01-19,15:24:22,2024-01-22,17:00:00,P0122001_S_150022-BKW-8,150022-BKW,\"SKECHERS - VAPOR FOAM 女裝運動鞋 (多款尺碼可供選購)\",1,\"SKECHERS - VAPOR FOAM WOMEN'S SPORT SHOES (Multiple Sizes Available)\",黑白色,Black/White,US 8,CONFIRMED,0.013104,6547428648,2024-01-23,Yes\nStandard Delivery,H240119040772,2024-01-19,15:58:53,2024-01-22,17:00:00,P0122001_S_150022-BKW-7,150022-BKW,\"SKECHERS - VAPOR FOAM 女裝運動鞋 (多款尺碼可供選購)\",1,\"SKECHERS - VAPOR FOAM WOMEN'S SPORT SHOES (Multiple Sizes Available)\",黑白色,Black/White,US 7,CONFIRMED,0.013104,6547490804,2024-01-23,No\nStandard Delivery,H240119092139,2024-01-19,22:43:17,2024-01-22,17:00:00,P0122001_S_117209-OFWT-7,117209-OFWT,\"SKECHERS - BOBS SQUAD CHAOS 女裝運動鞋 (多款尺碼可供選購)\",1,\"SKECHERS - BOBS SQUAD CHAOS WOMEN'S SPORT SHOES (Multiple Sizes Available)\",啡色,Natural,US 7,CONFIRMED,0.013104,6548380245,2024-01-23,No\nStandard Delivery,H240120008704,2024-01-20,13:18:35,2024-01-22,17:00:00,P0122001_S_104429-MVE-6,104429-MVE,\"SKECHERS - VIRTUE 女裝運動鞋 (多款尺碼可供選購)\",1,\"SKECHERS - VIRTUE WOMEN'S SPORT SHOES (Multiple Sizes Available)\",Suave Mauve,Suave Mauve,US 6,CONFIRMED,0.013104,6549145277,2024-01-23,Yes\nStandard Delivery,H240120009721,2024-01-20,14:05:36,2024-01-22,17:00:00,P0122001_S_P222W053-00FY-L,P222W053-00FY,\"SKECHERS - BASIC 女裝短袖衫 (多款尺碼可供選購)\",1,\"SKECHERS - BASIC WOMEN'S SHORT SLEEVE TEE (Multiple Sizes Available)\",珊瑚橙色,Coral,L,CONFIRMED,0.016848,6549199711,2024-01-23,No\nStandard Delivery,H240120009721,2024-01-20,14:05:36,2024-01-22,17:00:00,P0122001_S_128098-BKMT-8,128098-BKMT,\"SKECHERS - GO RUN HYPER BURST 女裝 跑步鞋 (多款尺碼可供選購)\",1,\"SKECHERS - GO RUN HYPER BURST WOMEN'S RUNNING SHOES (Multiple Sizes Available)\",黑色-彩色,Black-Multi Color,US 8,CONFIRMED,0.013104,6549199711,2024-01-23,No\nStandard Delivery,H240120029620,2024-01-20,15:26:00,2024-01-22,17:00:00,P0122001_S_302383L-BKHP-13,302383L-BKHP,\"SKECHERS - SKECH-AIR FUSION 女童運動鞋 (多款尺碼可供選購)\",1,\"SKECHERS - SKECH-AIR FUSION GIRLS' SPORT SHOES (Multiple Sizes Available)\",黑色/粉紅色,Black/Pink,US 13,CONFIRMED,0.016848,6549300241,2024-01-23,No\nStandard Delivery,H240120003972,2024-01-20,15:48:04,2024-01-22,17:00:00,P0122001_S_L223U016-02G4-M,L223U016-02G4,\"SKECHERS - FASHION 男女同款襪子 (3對裝) (多款尺碼可供選購)\",2,\"SKECHERS - FASHION UNISEX'S SOCKS (3 PAIRS) (Multiple Sizes Available)\",,,M,CONFIRMED,0.033696,6549328221,2024-01-23,Yes\nStandard Delivery,H240120022429,2024-01-20,17:13:44,2024-01-22,17:00:00,P0122001_S_314783L-BLMT-2,314783L-BLMT,\"SKECHERS - TWINKLE SPARKS ICE 女童閃燈鞋 (多款尺碼可供選購)\",1,\"SKECHERS - TWINKLE SPARKS ICE GIRLS' LIGHT UP SHOES (Multiple Sizes Available)\",藍色/彩色,Blue/Multi-Color,US 2,CONFIRMED,0.016848,6549443867,2024-01-23,No\nStandard Delivery,H240120022429,2024-01-20,17:13:44,2024-01-22,17:00:00,P0122001_S_314789L-WMLT-3,314789L-WMLT,\"SKECHERS - TWINKLE SPARKS 女童閃燈鞋 (多款尺碼可供選購)\",1,\"SKECHERS - TWINKLE SPARKS GIRLS' LIGHT UP SHOES (Multiple Sizes Available)\",白色/彩色,White/Multi-Color,US 3,CONFIRMED,0.016848,6549443867,2024-01-23,No\nStandard Delivery,H240120047179,2024-01-20,18:37:46,2024-01-22,17:00:00,P0122001_S_118034-W-9,118034-W,\"SKECHERS - BOBS SQUAD CHAOS 男裝運動鞋 (多款尺碼可供選購)\",1,\"SKECHERS - BOBS SQUAD CHAOS MEN'S SPORT SHOES (Multiple Sizes Available)\",白色,White,US 9,CONFIRMED,0.013104,6549558881,2024-01-23,No\nStandard Delivery,H240120047179,2024-01-20,18:37:46,2024-01-22,17:00:00,P0122001_S_232629-CCRD-11,232629-CCRD,\"SKECHERS - VAPOR FOAM 男裝運動鞋 (多款尺碼可供選購)\",1,\"SKECHERS - VAPOR FOAM MEN'S SPORT SHOES (Multiple Sizes Available)\",紅-炭灰色,Red-charcoal,US 11,CONFIRMED,0.013104,6549558881,2024-01-23,No\nStandard Delivery,H240120047179,2024-01-20,18:37:46,2024-01-22,17:00:00,P0122001_S_232625-WNVR-11,232625-WNVR,\"SKECHERS - VAPOR FOAM 男裝運動鞋 (多款尺碼可供選購)\",1,\"SKECHERS - VAPOR FOAM MEN'S SPORT SHOES (Multiple Sizes Available)\",白藍紅,White Blue Red,US 11,CONFIRMED,0.013104,6549558881,2024-01-23,No\nStandard Delivery,H240120047179,2024-01-20,18:37:46,2024-01-22,17:00:00,P0122001_S_52458-WNVR-9,52458-WNVR,\"SKECHERS - UNO 男裝時尚休閒鞋 (多款尺碼可供選購)\",1,\"SKECHERS - UNO MEN'S SNEAKERS (Multiple Sizes Available)\",白藍紅,White Blue Red,US 9,CONFIRMED,0.016848,6549558881,2024-01-23,No\nStandard Delivery,H240120048199,2024-01-20,18:54:51,2024-01-22,17:00:00,P0122001_S_129128-WPK-7,129128-WPK,\"SKECHERS - MAX CUSHIONING DELTA 女裝跑步鞋 (多款尺碼可供選購)\",1,\"SKECHERS - MAX CUSHIONING DELTA WOMEN'S RUNNING SHOES (Multiple Sizes Available)\",白色/粉紅色,White/Pink,US 7,CONFIRMED,0.016848,6549577724,2024-01-23,No\nStandard Delivery,H240120048199,2024-01-20,18:54:51,2024-01-22,17:00:00,P0122001_S_150022-NTMT-7,150022-NTMT,\"SKECHERS - VAPOR FOAM 女裝運動鞋 (多款尺碼可供選購)\",1,\"SKECHERS - VAPOR FOAM WOMEN'S SPORT SHOES (Multiple Sizes Available)\",米色/彩色,Beige/Multi-Color,US 7,CONFIRMED,0.013104,6549577724,2024-01-23,No\nStandard Delivery,H240120048236,2024-01-20,19:22:08,2024-01-22,17:00:00,P0122001_S_150022-GYMT-7,150022-GYMT,\"SKECHERS - VAPOR FOAM 女裝運動鞋 (多款尺碼可供選購)\",1,\"SKECHERS - VAPOR FOAM WOMEN'S SPORT SHOES (Multiple Sizes Available)\",灰色/彩色,Grey/Multi-Color,US 7,CONFIRMED,0.013104,6549610055,2024-01-23,No\nStandard Delivery,H240120048236,2024-01-20,19:22:08,2024-01-22,17:00:00,P0122001_S_104272-BKW-7,104272-BKW,\"SKECHERS - ARCH FIT REFINE 女裝運動鞋 (多款尺碼可供選購)\",1,\"SKECHERS - ARCH FIT REFINE WOMEN'S SPORT SHOES (Multiple Sizes Available)\",黑白色,Black/White,US 7,CONFIRMED,0.016848,6549610055,2024-01-23,No\nStandard Delivery,H240120051199,2024-01-20,19:42:13,2024-01-22,17:00:00,P0122001_S_124580-TPCL-5,124580-TPCL,\"SKECHERS - GO WALK HYPER BURST 女裝健步鞋 (多個尺碼可供選購)\",1,\"SKECHERS - GO WALK HYPER BURST WOMEN'S SHOES (Multiple Sizes Available)\",TAUPE PINK,TAUPE PINK,US 5,CONFIRMED,0.013104,6549632720,2024-01-23,No\nStandard Delivery,H240120051199,2024-01-20,19:42:13,2024-01-22,17:00:00,P0122001_S_150022-GYMT-5,150022-GYMT,\"SKECHERS - VAPOR FOAM 女裝運動鞋 (多款尺碼可供選購)\",1,\"SKECHERS - VAPOR FOAM WOMEN'S SPORT SHOES (Multiple Sizes Available)\",灰色/彩色,Grey/Multi-Color,US 5,CONFIRMED,0.013104,6549632720,2024-01-23,No\nStandard Delivery,H240120051199,2024-01-20,19:42:13,2024-01-22,17:00:00,P0122001_S_104272-BKW-7,104272-BKW,\"SKECHERS - ARCH FIT REFINE 女裝運動鞋 (多款尺碼可供選購)\",1,\"SKECHERS - ARCH FIT REFINE WOMEN'S SPORT SHOES (Multiple Sizes Available)\",黑白色,Black/White,US 7,CONFIRMED,0.016848,6549632720,2024-01-23,No\nStandard Delivery,H240120028997,2024-01-20,19:45:58,2024-01-22,17:00:00,P0122001_S_220034-BLYL-9,220034-BLYL,\"SKECHERS - GO RUN CONSISTENT 男裝跑步鞋 (多款尺碼可供選購)\",1,\"SKECHERS - GO RUN CONSISTENT MEN'S RUNNING SHOES (Multiple Sizes Available)\",藍色,Blue,US 9,CONFIRMED,0.013104,6549636853,2024-01-23,Yes\nStandard Delivery,H240120044340,2024-01-20,20:08:16,2024-01-22,17:00:00,P0122001_S_L223U016-02G4-M,L223U016-02G4,\"SKECHERS - FASHION 男女同款襪子 (3對裝) (多款尺碼可供選購)\",1,\"SKECHERS - FASHION UNISEX'S SOCKS (3 PAIRS) (Multiple Sizes Available)\",,,M,CONFIRMED,0.016848,6549660224,2024-01-23,No\nStandard Delivery,H240120051310,2024-01-20,20:57:02,2024-01-22,17:00:00,P0122001_S_108016EC-BLK-7,108016EC-BLK,\"SKECHERS - MAX CUSHIONING ELITE SR 女裝工作鞋 (多款尺碼可供選購)\",1,\"SKECHERS - MAX CUSHIONING ELITE SR WOMEN'S WORK SHOES (Multiple Sizes Available)\",黑色,Black,US 7,CONFIRMED,0.016848,6549716589,2024-01-23,Yes\nStandard Delivery,H240120051310,2024-01-20,20:57:02,2024-01-22,17:00:00,P0122001_S_108016-WHT-6,108016-WHT,\"SKECHERS - MAX CUSHIONING ELITE SR 女裝透氣工作鞋 (多款尺碼可供選購)\",1,\"SKECHERS - MAX CUSHIONING ELITE SR WOMEN'S WORK SHOES (Multiple Sizes Available)\",白色/白色,White/White,US 6,CONFIRMED,0.016848,6549716589,2024-01-23,Yes\nStandard Delivery,H240120017447,2024-01-20,21:08:14,2024-01-22,17:00:00,P0122001_S_104429-MVE-8,104429-MVE,\"SKECHERS - VIRTUE 女裝運動鞋 (多款尺碼可供選購)\",1,\"SKECHERS - VIRTUE WOMEN'S SPORT SHOES (Multiple Sizes Available)\",Suave Mauve,Suave Mauve,US 8,CONFIRMED,0.013104,6549717773,2024-01-23,Yes\nStandard Delivery,H240120049464,2024-01-20,22:07:57,2024-01-22,17:00:00,P0122001_S_216225-GRY-8,216225-GRY,\"SKECHERS - GO WALK GLIDE-STEP FLEX 男裝健步鞋 (多款尺碼可供選購)\",1,\"SKECHERS - GO WALK GLIDE-STEP FLEX MEN'S WALKING SHOES (Multiple Sizes Available)\",灰,Grey,US 8,CONFIRMED,0.013104,6549775426,2024-01-23,Yes\nStandard Delivery,H240120017490,2024-01-20,22:04:31,2024-01-22,17:00:00,P0122001_S_8750053-BKRG-7,8750053-BKRG,\"SKECHERS - ROSEATE 女裝運動鞋 (多款尺碼可供選購)\",1,\"SKECHERS - ROSEATE WOMEN'S SPORT SHOES (Multiple Sizes Available)\",黑/玫瑰金,Black/Rose Gold,US 7,CONFIRMED,0.016848,6549778203,2024-01-23,Yes\nStandard Delivery,H240120017490,2024-01-20,22:04:31,2024-01-22,17:00:00,P0122001_S_149750-NVCL-7,149750-NVCL,\"SKECHERS - SKECH-AIR DYNAMIGHT 女裝運動鞋 (多款尺碼可供選購)\",1,\"SKECHERS - SKECH-AIR DYNAMIGHT WOMEN'S SPORT SHOES (Multiple Sizes Available)\",,Pink/navy,US 7,CONFIRMED,0.013104,6549778203,2024-01-23,Yes\nStandard Delivery,H240120049470,2024-01-20,22:09:35,2024-01-22,17:00:00,P0122001_S_150041-BKPK-8,150041-BKPK,\"SKECHERS - SKECH-LITE PRO 女裝運動鞋 (多款尺碼可供選購)\",1,\"SKECHERS - SKECH-LITE PRO WOMEN'S SPORT SHOES (Multiple Sizes Available)\",黑色/粉紅色,Black/Pink,US 8,CONFIRMED,0.013104,6549781380,2024-01-23,Yes\nStandard Delivery,H240120067218,2024-01-20,22:14:21,2024-01-22,17:00:00,P0122001_S_216225-GRY-9,216225-GRY,\"SKECHERS - GO WALK GLIDE-STEP FLEX 男裝健步鞋 (多款尺碼可供選購)\",1,\"SKECHERS - GO WALK GLIDE-STEP FLEX MEN'S WALKING SHOES (Multiple Sizes Available)\",灰,Grey,US 9,CONFIRMED,0.013104,6549785619,2024-01-23,Yes\nStandard Delivery,H240120045642,2024-01-20,23:05:53,2024-01-22,17:00:00,P0122001_S_77108-BKCC-7,77108-BKCC,\"SKECHERS - HOLDREDGE 男裝工作鞋 (多款尺碼可供選購)\",1,\"SKECHERS - HOLDREDGE MEN'S WORK SHOES (Multiple Sizes Available)\",黑色/炭灰色,Black/Charcoal,US 7,CONFIRMED,0.016848,6549832515,2024-01-23,No\nStandard Delivery,H240120058377,2024-01-20,23:19:31,2024-01-22,17:00:00,P0122001_S_88888250-LPKW-8,88888250-LPKW,\"SKECHERS - I-CONIK 女裝休閒鞋 (多款尺碼可供選購)\",2,\"SKECHERS - I-CONIK SPORT SHOES (Multiple Sizes Available)\",粉紅色/白色,Pink/White,US 8,CONFIRMED,0.033696,6549844079,2024-01-23,No\nStandard Delivery,H240120058377,2024-01-20,23:19:31,2024-01-22,17:00:00,P0122001_S_88888250-LPKW-6,88888250-LPKW,\"SKECHERS - I-CONIK 女裝休閒鞋 (多款尺碼可供選購)\",1,\"SKECHERS - I-CONIK SPORT SHOES (Multiple Sizes Available)\",粉紅色/白色,Pink/White,US 6,CONFIRMED,0.016848,6549844079,2024-01-23,No\nStandard Delivery,H240120045681,2024-01-20,23:31:14,2024-01-22,17:00:00,P0122001_S_220034-BLYL-7,220034-BLYL,\"SKECHERS - GO RUN CONSISTENT 男裝跑步鞋 (多款尺碼可供選購)\",1,\"SKECHERS - GO RUN CONSISTENT MEN'S RUNNING SHOES (Multiple Sizes Available)\",藍色,Blue,US 7,CONFIRMED,0.013104,6549851403,2024-01-23,No\nStandard Delivery,H240121019006,2024-01-21,00:04:10,2024-01-22,17:00:00,P0122001_S_314432L-LVMT-2,314432L-LVMT,\"SKECHERS - TWI-LITES 2.0 女童閃燈鞋 (多款尺碼可供選購)\",1,\"SKECHERS - TWI-LITES 2.0 GIRLS' LIGHT UP SHOES (Multiple Sizes Available)\",紫色/彩色,Purple/Multi-Color,US 2,CONFIRMED,0.013104,6549873374,2024-01-23,Yes\nStandard Delivery,H240121019006,2024-01-21,00:04:10,2024-01-22,17:00:00,P0122001_S_400602N-NVMT-9,400602N-NVMT,\"SKECHERS - VORTEX 2.0 男幼童閃燈鞋 (多款尺碼可供選購)\",1,\"SKECHERS - VORTEX 2.0 MALE INFANTS' LIGHT UP SHOES (Multiple Sizes Available)\",藍色/彩色,Blue/Multi-Color,US 9,CONFIRMED,0.013104,6549873374,2024-01-23,Yes\nStandard Delivery,H240121009012,2024-01-21,00:08:08,2024-01-22,17:00:00,P0122001_S_302669L-PKLV-3,302669L-PKLV,\"SKECHERS - HEART LIGHTS 女童閃燈鞋 (多款尺碼可供選購)\",1,\"SKECHERS - HEART LIGHTS GIRLS' LIGHT UP SHOES (Multiple Sizes Available)\",粉橙,PEACH,US 3,CONFIRMED,0.013104,6549878717,2024-01-23,No\nStandard Delivery,H240121015044,2024-01-21,00:20:02,2024-01-22,17:00:00,P0122001_S_302207L-LVMT-3,302207L-LVMT,\"SKECHERS - QUICK KICKS 女童運動鞋 (多款尺碼可供選購)\",1,\"SKECHERS - QUICK KICKS GIRLS' SHOES (Multiple Sizes Available)\",紫色/彩色,Purple/Multi-Color,US 3,CONFIRMED,0.013104,6549883861,2024-01-23,Yes\nStandard Delivery,H240121015044,2024-01-21,00:20:02,2024-01-22,17:00:00,P0122001_S_302429L-WHT-4,302429L-WHT,\"SKECHERS - GO RUN 400 V2 女童運動鞋 (多款尺碼可供選購)\",1,\"SKECHERS - GO RUN 400 V2 GIRLS' SPORT SHOES (Multiple Sizes Available)\",白色,White,US 4,CONFIRMED,0.013104,6549883861,2024-01-23,Yes\nStandard Delivery,H240121015170,2024-01-21,02:42:53,2024-01-22,17:00:00,P0122001_S_52458-BLK-10,52458-BLK,\"SKECHERS - UNO 男裝 運動休閒鞋 (多款尺碼可供選購)\",1,\"SKECHERS - UNO MEN'S SNEAKERS (Multiple Sizes Available)\",黑色,Black,US 10,CONFIRMED,0.016848,6549943424,2024-01-23,No\nStandard Delivery,H240121026132,2024-01-21,08:35:38,2024-01-22,17:00:00,P0122001_S_232204-TPNV-10,232204-TPNV,\"SKECHERS - ARCH FIT 男裝運動鞋 (多款尺碼可供選購)\",1,\"SKECHERS - ARCH FIT MEN'S SPORT SHOES (Multiple Sizes Available)\",米色/藍色,Beige/Blue,US 10,CONFIRMED,0.016848,6549989671,2024-01-23,Yes\nStandard Delivery,H240121026132,2024-01-21,08:35:38,2024-01-22,17:00:00,P0122001_S_216225-NVY-10,216225-NVY,\"SKECHERS - GO WALK GLIDE-STEP FLEX 男裝健步鞋 (多款尺碼可供選購)\",1,\"SKECHERS - GO WALK GLIDE-STEP FLEX MEN'S WALKING SHOES (Multiple Sizes Available)\",深藍色,NAVY,US 10,CONFIRMED,0.013104,6549989671,2024-01-23,Yes\nStandard Delivery,H240121010234,2024-01-21,08:59:05,2024-01-22,17:00:00,P0122001_S_128075-GYLV-8,128075-GYLV,\"SKECHERS - GO RUN CONSISTENT 女裝跑步鞋 (多款尺碼可供選購)\",1,\"SKECHERS - GO RUN CONSISTENT WOMEN'S RUNNING SHOES (Multiple Sizes Available)\",灰白色/紫色,Grey/Purple,US 8,CONFIRMED,0.013104,6550003486,2024-01-23,Yes\nStandard Delivery,H240121002201,2024-01-21,09:25:51,2024-01-22,17:00:00,P0122001_S_82007L-WHT-2,82007L-WHT,\"SKECHERS - GO RUN 600 兒童返學鞋 (多款尺碼可供選購)\",1,\"SKECHERS - GO RUN 600 KIDS' SCHOOL SHOES (Multiple Sizes Available)\",白色,White,US 2,CONFIRMED,0.013104,6550016901,2024-01-23,Yes\nStandard Delivery,H240121009285,2024-01-21,09:52:14,2024-01-22,17:00:00,P0122001_S_220371-WNV-8,220371-WNV,\"SKECHERS - GO RUN CONSISTENT 男裝跑步鞋 (多款尺碼可供選購)\",1,\"SKECHERS - GO RUN CONSISTENT MEN'S RUNNING SHOES (Multiple Sizes Available)\",白色/海軍藍色,White/NavyBlue,US 8,CONFIRMED,0.013104,6550032165,2024-01-23,No\nStandard Delivery,H240121009285,2024-01-21,09:52:14,2024-01-22,17:00:00,P0122001_S_894073-WTGD-8,894073-WTGD,\"SKECHERS - STAMINA AIRY 男裝休閒鞋 (多款尺碼可供選購)\",1,\"SKECHERS - STAMINA AIRY MEN'S SPORT SHOES (Multiple Sizes Available)\",,,US 8,CONFIRMED,0.016848,6550032165,2024-01-23,No\nStandard Delivery,H240121007140,2024-01-21,09:54:55,2024-01-22,17:00:00,P0122001_S_88888250-LPKW-8,88888250-LPKW,\"SKECHERS - I-CONIK 女裝休閒鞋 (多款尺碼可供選購)\",1,\"SKECHERS - I-CONIK SPORT SHOES (Multiple Sizes Available)\",粉紅色/白色,Pink/White,US 8,CONFIRMED,0.016848,6550036485,2024-01-23,Yes\nStandard Delivery,H240121023167,2024-01-21,10:59:16,2024-01-22,17:00:00,P0122001_S_149854-NVY-6,149854-NVY,\"SKECHERS - ULTRA FLEX 3.0 女裝運動鞋 (多款尺碼可供選購)\",1,\"SKECHERS - ULTRA FLEX 3.0 WOMEN'S SPORT SHOES (Multiple Sizes Available)\",深藍色,NAVY,US 6,CONFIRMED,0.016848,6550089084,2024-01-23,No\nStandard Delivery,H240121023192,2024-01-21,11:43:16,2024-01-22,17:00:00,P0122001_S_220034-BLYL-8,220034-BLYL,\"SKECHERS - GO RUN CONSISTENT 男裝跑步鞋 (多款尺碼可供選購)\",1,\"SKECHERS - GO RUN CONSISTENT MEN'S RUNNING SHOES (Multiple Sizes Available)\",藍色,Blue,US 8,CONFIRMED,0.013104,6550137101,2024-01-23,Yes\nStandard Delivery,H240121009432,2024-01-21,11:43:52,2024-01-22,17:00:00,P0122001_S_8730065-TPE-6,8730065-TPE,\"SKECHERS - I-CONIK 女裝休閒鞋 (多款尺碼可供選購)\",1,\"SKECHERS - I-CONIK WOMEN'S SPORT SHOES (Multiple Sizes Available)\",灰褐色,Taupe,US 6,CONFIRMED,0.016848,6550137816,2024-01-23,Yes\nStandard Delivery,H240121004455,2024-01-21,11:57:28,2024-01-22,17:00:00,P0122001_S_L223U016-02G4-S,L223U016-02G4,\"SKECHERS - FASHION 男女同款襪子 (3對裝) (多款尺碼可供選購)\",2,\"SKECHERS - FASHION UNISEX'S SOCKS (3 PAIRS) (Multiple Sizes Available)\",,,S,CONFIRMED,0.033696,6550154004,2024-01-23,No\nStandard Delivery,H240121004455,2024-01-21,11:57:28,2024-01-22,17:00:00,P0122001_S_150022-NTMT-7,150022-NTMT,\"SKECHERS - VAPOR FOAM 女裝運動鞋 (多款尺碼可供選購)\",1,\"SKECHERS - VAPOR FOAM WOMEN'S SPORT SHOES (Multiple Sizes Available)\",米色/彩色,Beige/Multi-Color,US 7,CONFIRMED,0.013104,6550154004,2024-01-23,No\nStandard Delivery,H240121011192,2024-01-21,12:01:28,2024-01-22,17:00:00,P0122001_S_125231-BKW-6,125231-BKW,\"SKECHERS - SLIP INS 速穿科技: GO WALK 7 女裝健步鞋 (多款尺碼可供選購)\",1,\"SKECHERS - SLIP INS: GO WALK 7 WOMEN'S WALKING SHOES (Multiple Sizes Available)\",黑白色,Black/White,US 6,CONFIRMED,0.013104,6550158182,2024-01-23,No\nStandard Delivery,H240121011192,2024-01-21,12:01:28,2024-01-22,17:00:00,P0122001_S_125233-NVLV-8,125233-NVLV,\"SKECHERS - SLIP INS 速穿科技: GO WALK 7 女裝健步鞋 (多款尺碼可供選購)\",1,\"SKECHERS - SLIP INS: GO WALK 7 WOMEN'S WALKING SHOES (Multiple Sizes Available)\",,Purple/Navy,US 8,CONFIRMED,0.013104,6550158182,2024-01-23,No\nStandard Delivery,H240121012485,2024-01-21,12:33:12,2024-01-22,17:00:00,P0122001_S_118034-W-8,118034-W,\"SKECHERS - BOBS SQUAD CHAOS 男裝運動鞋 (多款尺碼可供選購)\",1,\"SKECHERS - BOBS SQUAD CHAOS MEN'S SPORT SHOES (Multiple Sizes Available)\",白色,White,US 8,CONFIRMED,0.013104,6550197563,2024-01-23,Yes\nStandard Delivery,H240121026408,2024-01-21,12:40:22,2024-01-22,17:00:00,P0122001_S_8730066-WLGY-7,8730066-WLGY,\"SKECHERS - I-CONIK 女裝休閒鞋 (多款尺碼可供選購)\",1,\"SKECHERS - I-CONIK WOMEN'S CASUAL SHOES (Multiple Sizes Available)\",白色,White,US 7,CONFIRMED,0.013104,6550207180,2024-01-23,No\nStandard Delivery,H240121026408,2024-01-21,12:40:22,2024-01-22,17:00:00,P0122001_S_220371-WNV-9-5,220371-WNV,\"SKECHERS - GO RUN CONSISTENT 男裝跑步鞋 (多款尺碼可供選購)\",1,\"SKECHERS - GO RUN CONSISTENT MEN'S RUNNING SHOES (Multiple Sizes Available)\",白色/海軍藍色,White/NavyBlue,US 9.5,CONFIRMED,0.013104,6550207180,2024-01-23,No\nStandard Delivery,H240121026408,2024-01-21,12:40:22,2024-01-22,17:00:00,P0122001_S_220371-WNV-7-5,220371-WNV,\"SKECHERS - GO RUN CONSISTENT 男裝跑步鞋 (多款尺碼可供選購)\",1,\"SKECHERS - GO RUN CONSISTENT MEN'S RUNNING SHOES (Multiple Sizes Available)\",白色/海軍藍色,White/NavyBlue,US 7.5,CONFIRMED,0.013104,6550207180,2024-01-23,No\nStandard Delivery,H240121026408,2024-01-21,12:40:22,2024-01-22,17:00:00,P0122001_S_8730066-WLGY-8,8730066-WLGY,\"SKECHERS - I-CONIK 女裝休閒鞋 (多款尺碼可供選購)\",1,\"SKECHERS - I-CONIK WOMEN'S CASUAL SHOES (Multiple Sizes Available)\",白色,White,US 8,CONFIRMED,0.013104,6550207180,2024-01-23,No\nStandard Delivery,H240121006549,2024-01-21,13:18:47,2024-01-22,17:00:00,P0122001_S_149253-BKMT-7,149253-BKMT,\"SKECHERS - D'LITES 女裝 運動休閒鞋 (多款尺碼可供選購)\",1,\"SKECHERS - D'LITES WOMEN'S SHOES (Multiple Sizes Available)\",黑色-彩色,Black-Multi Color,US 7,CONFIRMED,0.016848,6550251286,2024-01-23,No\nStandard Delivery,H240121006549,2024-01-21,13:18:47,2024-01-22,17:00:00,P0122001_S_302713N-LVMT-10,302713N-LVMT,\"SKECHERS - COMFY FLEX 2.0 女幼童運動鞋 (多款尺碼可供選購)\",1,\"SKECHERS - COMFY FLEX 2.0 FEMALE INFANTS' SPORT SHOES (Multiple Sizes Available)\",紫色/彩色,Purple/Multi-Color,US 10,CONFIRMED,0.013104,6550251286,2024-01-23,No\nStandard Delivery,H240121002515,2024-01-21,13:25:10,2024-01-22,17:00:00,P0122001_S_104429-NVY-8,104429-NVY,\"SKECHERS - VIRTUE 女裝運動鞋 (多款尺碼可供選購)\",1,\"SKECHERS - VIRTUE WOMEN'S SPORT SHOES (Multiple Sizes Available)\",深藍色,NAVY,US 8,CONFIRMED,0.013104,6550258605,2024-01-23,No\nStandard Delivery,H240121016649,2024-01-21,14:16:44,2024-01-22,17:00:00,P0122001_S_128075-GYLV-7,128075-GYLV,\"SKECHERS - GO RUN CONSISTENT 女裝跑步鞋 (多款尺碼可供選購)\",1,\"SKECHERS - GO RUN CONSISTENT WOMEN'S RUNNING SHOES (Multiple Sizes Available)\",灰白色/紫色,Grey/Purple,US 7,CONFIRMED,0.013104,6550318759,2024-01-23,No\nStandard Delivery,H240121012622,2024-01-21,14:17:38,2024-01-22,17:00:00,P0122001_S_8750053-BKRG-7,8750053-BKRG,\"SKECHERS - ROSEATE 女裝運動鞋 (多款尺碼可供選購)\",1,\"SKECHERS - ROSEATE WOMEN'S SPORT SHOES (Multiple Sizes Available)\",黑/玫瑰金,Black/Rose Gold,US 7,CONFIRMED,0.016848,6550321345,2024-01-23,Yes\nStandard Delivery,H240121006663,2024-01-21,14:34:27,2024-01-22,17:00:00,P0122001_S_220082-BKBL-9,220082-BKBL,\"SKECHERS - GO RUN CONSISTENT 男裝 跑步鞋 (多個尺碼可供選購)\",1,\"SKECHERS - GO RUN CONSISTENT MEN'S RUNNING SHOES\",黑色/藍色,Black/Blue,US 9,CONFIRMED,0.013104,6550344295,2024-01-23,No\nStandard Delivery,H240121013653,2024-01-21,15:15:29,2024-01-22,17:00:00,P0122001_S_104429-NVY-7,104429-NVY,\"SKECHERS - VIRTUE 女裝運動鞋 (多款尺碼可供選購)\",1,\"SKECHERS - VIRTUE WOMEN'S SPORT SHOES (Multiple Sizes Available)\",深藍色,NAVY,US 7,CONFIRMED,0.013104,6550398524,2024-01-23,No\nStandard Delivery,H240121019828,2024-01-21,15:34:39,2024-01-22,17:00:00,P0122001_S_99999720-BKW-6,99999720-BKW,\"SKECHERS - D'LITES 女裝 休閒鞋 (多款尺碼可供選購)\",1,\"SKECHERS - D'LITES WOMEN'S SHOES (Multiple Sizes Available)\",黑白色,Black/White,US 6,CONFIRMED,0.016848,6550427342,2024-01-23,No\nStandard Delivery,H240121015828,2024-01-21,15:39:04,2024-01-22,17:00:00,P0122001_S_314764L-NVMT-2,314764L-NVMT,\"SKECHERS - SPARKLE LITE 女童閃燈鞋 (多款尺碼可供選購)\",1,\"SKECHERS - SPARKLE LITE GIRLS' LIGHT UP SHOES (Multiple Sizes Available)\",藍色/彩色,Blue/Multi-Color,US 2,CONFIRMED,0.013104,6550430652,2024-01-23,No\nStandard Delivery,H240121013694,2024-01-21,15:47:56,2024-01-22,17:00:00,P0122001_S_P223U006-02Z2-M,P223U006-02Z2,\"SKECHERS - BASIC 男女同款襪子 (2對裝) (多款尺碼可供選購)\",2,\"SKECHERS - BASIC UNISEX'S SOCKS (2 PAIRS) (Multiple Sizes Available)\",,,M,CONFIRMED,0.033696,6550442830,2024-01-23,Yes\nStandard Delivery,H240121013694,2024-01-21,15:47:56,2024-01-22,17:00:00,P0122001_S_216202-BLK-10,216202-BLK,\"SKECHERS - GO WALK 6 男裝健步鞋 (多款尺碼可供選購)\",1,\"SKECHERS - GO WALK 6 MEN'S WALKING SHOES (Multiple Sizes Available)\",黑色,Black,US 10,CONFIRMED,0.016848,6550442830,2024-01-23,Yes\nStandard Delivery,H240121000854,2024-01-21,15:58:26,2024-01-22,17:00:00,P0122001_S_8730066-WLGY-7,8730066-WLGY,\"SKECHERS - I-CONIK 女裝休閒鞋 (多款尺碼可供選購)\",1,\"SKECHERS - I-CONIK WOMEN'S CASUAL SHOES (Multiple Sizes Available)\",白色,White,US 7,CONFIRMED,0.013104,6550453413,2024-01-23,No\nStandard Delivery,H240121004854,2024-01-21,16:24:26,2024-01-22,17:00:00,P0122001_S_220082-WBOR-7,220082-WBOR,\"SKECHERS - GO RUN CONSISTENT 男裝跑步鞋 (多款尺碼可供選購)\",1,\"SKECHERS - GO RUN CONSISTENT MEN'S RUNNING SHOES (Multiple Sizes Available)\",白/藍,White/Blue,US 7,CONFIRMED,0.013104,6550490925,2024-01-23,Yes\nStandard Delivery,H240121006834,2024-01-21,16:40:38,2024-01-22,17:00:00,P0122001_S_117209-OFWT-7,117209-OFWT,\"SKECHERS - BOBS SQUAD CHAOS 女裝運動鞋 (多款尺碼可供選購)\",1,\"SKECHERS - BOBS SQUAD CHAOS WOMEN'S SPORT SHOES (Multiple Sizes Available)\",啡色,Natural,US 7,CONFIRMED,0.013104,6550514395,2024-01-23,Yes\nStandard Delivery,H240121006834,2024-01-21,16:40:38,2024-01-22,17:00:00,P0122001_S_149787-BKW-7,149787-BKW,\"SKECHERS - D'LITES 女裝休閒運動涼鞋\",1,\"SKECHERS - D'LITES WOMEN'S SANDALS\",黑白色,Black/White,US 7,CONFIRMED,0.013104,6550514395,2024-01-23,Yes\nStandard Delivery,H240121011387,2024-01-21,16:51:36,2024-01-22,17:00:00,P0122001_S_L323U117-002Z-99,L323U117-002Z,\"SKECHERS - FASHION 男女同款背包 (多款尺碼可供選購)\",1,\"SKECHERS - FASHION UNISEX'S BACKPACK (Multiple Sizes Available)\",藍色,Blue,,CONFIRMED,0.013104,6550530228,2024-01-23,Yes\nStandard Delivery,H240121018971,2024-01-21,17:07:33,2024-01-22,17:00:00,P0122001_S_896078-OFWT-5,896078-OFWT,\"SKECHERS - STAMINA AIRY 女裝運動鞋 (多款尺碼可供選購)\",1,\"SKECHERS - STAMINA AIRY WOMEN'S SPORT SHOES (Multiple Sizes Available)\",啡色,Natural,US 5,CONFIRMED,0.013104,6550552948,2024-01-23,Yes\nStandard Delivery,H240121010948,2024-01-21,17:09:48,2024-01-22,17:00:00,P0122001_S_117356-NTMT-7,117356-NTMT,\"SKECHERS - BOBS BAMINA 女裝運動鞋 (多款尺碼可供選購)\",1,\"SKECHERS - BOBS BAMINA WOMEN'S SPORT SHOES (Multiple Sizes Available)\",米色/彩色,Beige/Multi-Color,US 7,CONFIRMED,0.013104,6550557809,2024-01-23,No\nStandard Delivery,H240121010948,2024-01-21,17:09:48,2024-01-22,17:00:00,P0122001_S_13169-BKW-7,13169-BKW,\"SKECHERS - D'LITES 1.0 女裝休閒休閒鞋 (多款尺碼可供選購)\",1,\"SKECHERS - D'LITES 1.0 WOMEN'S SNEAKERS (Multiple Sizes Available)\",黑白色,Black/White,US 7,CONFIRMED,0.016848,6550557809,2024-01-23,No\nStandard Delivery,H240121009903,2024-01-21,17:24:08,2024-01-22,17:00:00,P0122001_S_150022-GYMT-7,150022-GYMT,\"SKECHERS - VAPOR FOAM 女裝運動鞋 (多款尺碼可供選購)\",1,\"SKECHERS - VAPOR FOAM WOMEN'S SPORT SHOES (Multiple Sizes Available)\",灰色/彩色,Grey/Multi-Color,US 7,CONFIRMED,0.013104,6550575861,2024-01-23,No\nStandard Delivery,H240121009903,2024-01-21,17:24:08,2024-01-22,17:00:00,P0122001_S_104429-MVE-7,104429-MVE,\"SKECHERS - VIRTUE 女裝運動鞋 (多款尺碼可供選購)\",1,\"SKECHERS - VIRTUE WOMEN'S SPORT SHOES (Multiple Sizes Available)\",Suave Mauve,Suave Mauve,US 7,CONFIRMED,0.013104,6550575861,2024-01-23,No\nStandard Delivery,H240121009903,2024-01-21,17:24:08,2024-01-22,17:00:00,P0122001_S_104429-NVY-7,104429-NVY,\"SKECHERS - VIRTUE 女裝運動鞋 (多款尺碼可供選購)\",1,\"SKECHERS - VIRTUE WOMEN'S SPORT SHOES (Multiple Sizes Available)\",深藍色,NAVY,US 7,CONFIRMED,0.013104,6550575861,2024-01-23,No\nStandard Delivery,H240121050023,2024-01-21,17:38:14,2024-01-22,17:00:00,P0122001_S_118034-W-8,118034-W,\"SKECHERS - BOBS SQUAD CHAOS 男裝運動鞋 (多款尺碼可供選購)\",1,\"SKECHERS - BOBS SQUAD CHAOS MEN'S SPORT SHOES (Multiple Sizes Available)\",白色,White,US 8,CONFIRMED,0.013104,6550597018,2024-01-23,No\nStandard Delivery,H240121049015,2024-01-21,17:40:07,2024-01-22,17:00:00,P0122001_S_104259-BKW-9,104259-BKW,\"SKECHERS - SKECH-AIR ARCH FIT 女裝運動鞋 (多款尺碼可供選購)\",1,\"SKECHERS - SKECH-AIR ARCH FIT WOMEN'S SPORT SHOES (Multiple Sizes Available)\",黑白色,Black/White,US 9,CONFIRMED,0.016848,6550598944,2024-01-23,No\nStandard Delivery,H240121010998,2024-01-21,17:44:47,2024-01-22,17:00:00,P0122001_S_77200-BLK-7,77200-BLK,\"SKECHERS - DIGHTON 女裝電氣絕緣抗滑工作鞋 (多款尺碼可供選購)\",1,\"SKECHERS - DIGHTON WOMEN'S WORK SHOES (Multiple Sizes Available)\",黑色/黑色,Black/Black,US 7,CONFIRMED,0.016848,6550604081,2024-01-23,No\nStandard Delivery,H240121010998,2024-01-21,17:44:47,2024-01-22,17:00:00,P0122001_S_L322U077-00CC-M,L322U077-00CC,\"SKECHERS - FASHION 男女同款短襪 (3對裝) (多款尺碼可供選購)\",1,\"SKECHERS - FASHION UNISEX'S QUARTER SOCK (3 PAIRS) (Multiple Sizes Available)\",,,M,CONFIRMED,0.016848,6550604081,2024-01-23,No"

class DataFormatEnumTest(unittest.TestCase):
    def test_formatToJson_CSV(self):
        self.assertEqual(94, len(TextFormatUtil.getDataFormatEnum(csv_text_data).formatToJson(csv_text_data)))

if __name__ == '__main__':
    unittest.main()