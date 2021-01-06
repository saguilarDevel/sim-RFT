
from collections import defaultdict
import math


def TOA_dic_calculation(results_dic):
    
    TOA_calculation_result = defaultdict(float)   
    prov1 = 0
    prov2 = 0
    for i in results_dic:
        #i is ack size
        print str(i)+", " + str(results_dic[i])+", "  + str(TOA_calculation(i))
        TOA_calculation_result[i] = TOA_calculation(i)
        prov1 = prov1 + (TOA_calculation(i)*results_dic[i])
        prov2 = prov2 + results_dic[i]
    return prov1 / prov2

    #print TOA_calculation_result
    #raw_input('')

    #return TOA_calculation_result

def TOA_dic_calculation_sd(results_dic):
    
    TOA_calculation_result = defaultdict(float)   
    prov1 = 0
    prov2 = 0
    for i in results_dic:
        #i is ack size
        print str(i)+", results_dic-> " + str(results_dic[i])+", TOA_calculation-> "  + str(TOA_calculation(i))
        TOA_calculation_result[TOA_calculation(i)] = results_dic[i]
        prov1 = prov1 + (TOA_calculation(i)*results_dic[i])
        prov2 = prov2 + results_dic[i]
    #return prov1 / prov2
    print prov1 / prov2

    print TOA_calculation_result

    sum_of_numbers = sum(number*count for number, count in TOA_calculation_result.iteritems())
    count = sum(count for n, count in TOA_calculation_result.iteritems())
    print sum_of_numbers
    print count
    mean = sum_of_numbers / count
    print mean
    total_squares = sum(number*number * count for number, count in TOA_calculation_result.iteritems())
    mean_of_squares = total_squares / count
    variance = mean_of_squares - mean * mean
    std_dev = math.sqrt(variance)
    print variance
    print std_dev
    return std_dev


def TOA_dic_calculation_variance(results_dic):
    
    TOA_calculation_result = defaultdict(float)   
    prov1 = 0
    prov2 = 0
    for i in results_dic:
        #i is ack size
        print str(i)+", results_dic-> " + str(results_dic[i])+", TOA_calculation-> "  + str(TOA_calculation(i))
        TOA_calculation_result[TOA_calculation(i)] = results_dic[i]
        prov1 = prov1 + (TOA_calculation(i)*results_dic[i])
        prov2 = prov2 + results_dic[i]
    #return prov1 / prov2
    print prov1 / prov2

    print TOA_calculation_result

    sum_of_numbers = sum(number*count for number, count in TOA_calculation_result.iteritems())
    count = sum(count for n, count in TOA_calculation_result.iteritems())
    print sum_of_numbers
    print count
    mean = sum_of_numbers / count
    print mean
    total_squares = sum(number*number * count for number, count in TOA_calculation_result.iteritems())
    mean_of_squares = total_squares / count
    variance = mean_of_squares - mean * mean
    std_dev = math.sqrt(variance)
    print variance
    print std_dev
    return variance
    #print TOA_calculation_result
    #raw_input('')

    #return TOA_calculation_result

def TOA_calculation(ack_size):
    ''' Receives an ack size and returns the time on air for LORAWAN
        SF = 10, 
    '''
    TOA = defaultdict(float)
    TOA = {
        0:288.768,
        1:329.728,
        2:329.728,
        3:329.728,
        4:329.728,
        5:329.728,
        6:370.688,
        7:370.688,
        8:370.688,
        9:370.688,
        10:370.688,
        11:659.456,
        12:700.416,
        13:700.416,
        14:700.416,
        15:700.416,
        16:700.416,
        17:741.376,
        18:741.376,
        19:741.376,
        20:741.376,
        21:741.376,
        22:1030.144,
        23:1071.104,
        24:1071.104,
        25:1071.104,
        26:1071.104,
        27:1071.104,
        28:1112.064,
        29:1112.064,
        30:1112.064,
        31:1112.064,
        32:1112.064,
        33:1400.832,
        34:1441.792,
        35:1441.792,
        36:1441.792,
        37:1441.792,
        38:1441.792,
        39:1482.752,
        40:1482.752,
        41:1482.752,
        42:1482.752,
        43:1482.752,
        44:1771.52,
        45:1812.48,
        46:1812.48,
        47:1812.48,
        48:1812.48,
        49:1812.48,
        50:1853.44,
        51:1853.44,
        52:1853.44,
        53:1853.44,
        54:1853.44,
        55:2142.208,
        56:2183.168,
        57:2183.168,
        58:2183.168,
        59:2183.168,
        60:2183.168,
        61:2224.128,
        62:2224.128,
        63:2224.128,
        64:2224.128,
        65:2224.128,
        66:2512.896,
        67:2553.856,
        68:2553.856,
        69:2553.856,
        70:2553.856,
        71:2553.856,
        72:2594.816,
        73:2594.816,
        74:2594.816,
        75:2594.816,
        76:2594.816,
        77:2883.584,
        78:2924.544,
        79:2924.544,
        80:2924.544,
        81:2924.544,
        82:2924.544,
        83:2965.504,
        84:2965.504,
        85:2965.504,
        86:2965.504,
        87:2965.504,
        88:3254.272,
        89:3295.232,
        90:3295.232,
        91:3295.232,
        92:3295.232,
        93:3295.232,
        94:3336.192,
        95:3336.192,
        96:3336.192,
        97:3336.192,
        98:3336.192,
        # 0:0.288768,
        # 1:0.329728,
        # 2:0.329728,
        # 3:0.329728,
        # 4:0.329728,
        # 5:0.329728,
        # 6:0.370688,
        # 7:0.370688,
        # 8:0.370688,
        # 9:0.370688,
        # 10:0.370688,
        # 11:0.577536,
        # 12:0.618496,
        # 13:0.618496,
        # 14:0.618496,
        # 15:0.618496,
        # 16:0.618496,
        # 17:0.659456,
        # 18:0.659456,
        # 19:0.659456,
        # 20:0.659456,
        # 21:0.866304,
        # 22:0.866304,
        # 23:0.907264,
        # 24:0.907264,
        # 25:0.907264,
        # 26:0.907264,
        # 27:0.907264,
        # 28:0.948224,
        # 29:0.948224,
        # 30:0.948224,
        # 31:1.155072,
        # 32:1.155072,
        # 33:1.155072,
        # 34:1.196032,
        # 35:1.196032,
        # 36:1.196032,
        # 37:1.196032,
        # 38:1.196032,
        # 39:1.236992,
        # 40:1.425408,
        # 41:1.52576,
        # 42:1.52576,
        # 43:1.52576,
        # 44:1.56672,
        # 45:1.56672,
        # 46:1.56672,
        # 47:1.56672,
        # 48:1.56672,
        # 49:1.60768,
        # 50:1.896448,
        # 51:1.896448,
        # 52:1.896448,
        # 53:1.896448,
        # 54:1.937408,
        # 55:1.937408,
        # 56:1.937408,
        # 57:1.937408,
        # 58:1.937408,
        # 59:1.978368,
        # 60:2.267136,
        # 61:2.267136,
        # 62:2.267136,
        # 63:2.267136,
        # 64:2.308096,
        # 65:2.308096,
        # 66:2.308096,
        # 67:2.308096,
        # 68:2.308096,
        # 69:2.349056,
        # 70:2.637824,
        # 71:2.637824,
        # 72:2.637824,
        # 73:2.637824,
        # 74:2.678784,
        # 75:2.678784,
        # 76:2.678784,
        # 77:2.678784,
        # 78:2.678784,
        # 79:2.719744,
        # 80:3.008512,
        # 81:3.008512,
        # 82:3.008512,
        # 83:3.008512,
        # 84:3.049472,
        # 85:3.049472,
        # 86:3.049472,
        # 87:3.049472,
        # 88:3.049472,
        # 89:3.090432,
        # 90:3.3792,
        # 91:3.3792,
        # 92:3.3792,
        # 93:3.3792,
        # 94:3.42016,
        # 95:3.42016,
        # 96:3.42016,
        # 97:3.42016,
        # 98:3.42016,
        # 99:3.46112,
        # 100:3.749888,
        # 101:3.749888,
        # 102:3.749888,
        # 103:3.749888,
        # 104:3.790848,
        # 105:3.790848,
        # 106:3.790848,
        # 107:3.790848,
        # 108:3.790848,
        # 109:3.831808,
        # 110:4.120576,
        # 111:4.120576,
        # 112:4.120576,
        # 113:4.120576,
        # 114:4.161536,
        # 115:4.161536,
        # 116:4.161536,
        # 117:4.161536,
        # 118:4.161536,
        # 119:4.202496,
        # 120:4.491264,
        # 121:4.491264,
        # 122:4.491264,
        # 123:4.491264,
        # 124:4.532224,
        # 125:4.532224,
        # 126:4.532224,
        # 127:4.532224,
        # 128:4.532224,
        # 129:4.573184,
        # 130:4.861952,
        # 131:4.861952,
        # 132:4.861952,
        # 133:4.861952,
        # 134:4.902912,
        # 135:4.902912,
        # 136:4.902912,
        # 137:4.902912,
        # 138:4.902912,
        # 139:4.943872,
        # 140:5.23264,
        # 141:5.23264,
        # 142:5.23264,
        # 143:5.23264,
        # 144:5.2736,
        # 145:5.2736,
        # 146:5.2736,
        # 147:5.2736,
        # 148:5.2736,
        # 149:5.31456,
        # 150:5.603328,
        # 151:5.603328,
        # 152:5.603328,
        # 153:5.603328,
        # 154:5.644288,
        # 155:5.644288,
        # 156:5.644288,
        # 157:5.644288,
        # 158:5.644288,
        # 159:5.685248,
        # 160:5.974016,
        # 161:5.974016,
        # 162:5.974016,
        # 163:5.974016,
        # 164:6.014976,
        # 165:6.014976,
        # 166:6.014976,
        # 167:6.014976,
        # 168:6.014976,
        # 169:6.055936,
        # 170:6.344704,
        # 171:6.344704,
        # 172:6.344704,
        # 173:6.344704,
        # 174:6.385664,
        # 175:6.385664,
        # 176:6.385664,
        # 177:6.385664,
        # 178:6.385664,
        # 179:6.426624,
        # 180:6.715392,
        # 181:6.715392,
        # 182:6.715392,
        # 183:6.715392,
        # 184:6.756352,
        # 185:6.756352,
        # 186:6.756352,
        # 187:6.756352,
        # 188:6.756352,
        # 189:6.797312,
        # 190:7.08608,
        # 191:7.08608,
        # 192:7.08608,
        # 193:7.08608,
        # 194:7.12704,
        # 195:7.12704,
        # 196:7.12704,
        # 197:7.12704,
        # 198:7.12704,
        # 199:7.168,
        # 200:7.456768,
        # 201:7.456768,
        # 202:7.456768,
        # 203:7.456768,
        # 204:7.497728,
        # 205:7.497728,
        # 206:7.497728,
        # 207:7.497728,
        # 208:7.497728,
        # 209:7.538688,
        # 210:7.827456,
        # 211:7.827456,
        # 212:7.827456,
        # 213:7.827456,
        # 214:7.868416,
        # 215:7.868416,
        # 216:7.868416,
        # 217:7.868416,
        # 218:7.868416,
        # 219:7.909376,
        # 220:8.198144,
        # 221:8.198144,
        # 222:8.198144,
        # 223:8.198144,
        # 224:8.239104,
        # 225:8.239104,
        # 226:8.239104,
        # 227:8.239104,
        # 228:8.239104,
        # 229:8.280064,
        # 230:8.568832,
        # 231:8.568832,
        # 232:8.568832,
        # 233:8.568832,
        # 234:8.609792,
        # 235:8.609792,
        # 236:8.609792,
        # 237:8.609792,
        # 238:8.609792,
        # 239:8.650752,
        # 240:8.93952,
        # 241:8.93952,
        # 242:8.93952,
        # 243:8.93952,
        # 244:8.98048,
        # 245:8.98048,
        # 246:8.98048,
        # 247:8.98048,
        # 248:8.98048,
        # 249:9.02144,
        # 250:9.310208,
        # 251:9.310208,
        # 252:9.310208,
        # 253:9.310208,
        # 254:9.351168,
        # 255:9.351168,
        # 256:9.351168,
        # 257:9.351168,
        # 258:9.351168,
        # 259:9.392128,
        # 260:9.680896,
        # 261:9.680896,
        # 262:9.680896,
        # 263:9.680896,
        # 264:9.721856,
        # 265:9.721856,
        # 266:9.721856,
        # 267:9.721856,
        # 268:9.721856,
        # 269:9.762816,
        # 270:10.051584,
        # 271:10.051584,
        # 272:10.051584,
        # 273:10.051584,
        # 274:10.092544,
        # 275:10.092544,
        # 276:10.092544,
        # 277:10.092544,
        # 278:10.092544,
        # 279:10.133504,
        # 280:10.422272,
        # 281:10.422272,
        # 282:10.422272,
        # 283:10.422272,
        # 284:10.463232,
        # 285:10.463232,
        # 286:10.463232,
        # 287:10.463232,
        # 288:10.463232,
        # 289:10.504192,
        # 290:10.79296,
        # 291:10.79296,
        # 292:10.79296,
        # 293:10.79296,
        # 294:10.83392,
        # 295:10.83392,
        # 296:10.83392,
        # 297:10.83392,
        # 298:10.83392,
        # 299:10.87488,
        # 300:11.163648,
        # 301:11.163648,
        # 302:11.163648,
        # 303:11.163648,
        # 304:11.204608,
        # 305:11.204608,
        # 306:11.204608,
        # 307:11.204608,
        # 308:11.204608,
        # 309:11.245568,
        # 310:11.534336,
        # 311:11.534336,
        # 312:11.534336,
        # 313:11.534336,
        # 314:11.575296,
        # 315:11.575296,
        # 316:11.575296,
        # 317:11.575296,
        # 318:11.575296,
        # 319:11.616256,
        # 320:11.905024,
        # 321:11.905024,
        # 322:11.905024,
        # 323:11.905024,
        # 324:11.945984,
        # 325:11.945984,
        # 326:11.945984,
        # 327:11.945984,
        # 328:11.945984,
        # 329:11.986944,
        # 330:12.275712,
        # 331:12.275712,
        # 332:12.275712,
        # 333:12.275712,
        # 334:12.316672,
        # 335:12.316672,
        # 336:12.316672,
        # 337:12.316672,
        # 338:12.316672,
        # 339:12.357632,
        # 340:12.6464,
        # 341:12.6464,
        # 342:12.6464,
        # 343:12.6464,
        # 344:12.68736,
        # 345:12.68736,
        # 346:12.68736,
        # 347:12.68736,
        # 348:12.68736,
        # 349:12.72832,
        # 350:13.017088,
        # 351:13.017088,
        # 352:13.017088,
        # 353:13.017088,
        # 354:13.058048,
        # 355:13.058048,
        # 356:13.058048,
        # 357:13.058048,
        # 358:13.058048,
        # 359:13.099008,
        # 360:13.387776,
        # 361:13.387776,
        # 362:13.387776,
        # 363:13.387776,
        # 364:13.428736,
        # 365:13.428736,
        # 366:13.428736,
        # 367:13.428736,
        # 368:13.428736,
        # 369:13.469696,
        # 370:13.758464,
        # 371:13.758464,
        # 372:13.758464,
        # 373:13.758464,
        # 374:13.799424,
        # 375:13.799424,
        # 376:13.799424,
        # 377:13.799424,
        # 378:13.799424,
        # 379:13.840384,
        # 380:14.129152,
        # 381:14.129152,
        # 382:14.129152,
        # 383:14.129152,
        # 384:14.170112,
        # 385:14.170112,
        # 386:14.170112,
        # 387:14.170112,
        # 388:14.170112,
        # 389:14.211072,
        # 390:14.49984,
        # 391:14.49984,
        # 392:14.49984,
        # 393:14.49984,
        # 394:14.5408,
        # 395:14.5408,
        # 396:14.5408,
        # 397:14.5408,
        # 398:14.5408,
        # 399:14.58176,
        # 400:14.870528,
        # 401:14.870528,
        # 402:14.870528,
        # 403:14.870528,
        # 404:14.911488,
        # 405:14.911488,
        # 406:14.911488,
        # 407:14.911488,
        # 408:14.911488,
        # 409:14.952448,
        # 410:15.241216,
        # 411:15.241216,
        # 412:15.241216,
        # 413:15.241216,
        # 414:15.282176,
        # 415:15.282176,
        # 416:15.282176,
        # 417:15.282176,
        # 418:15.282176,
        # 419:15.323136,
        # 420:15.611904,
        # 421:15.611904,
        # 422:15.611904,
        # 423:15.611904,
        # 424:15.652864,
        # 425:15.652864,
        # 426:15.652864,
        # 427:15.652864,
        # 428:15.652864,
        # 429:15.693824,
        # 430:15.982592,
        # 431:15.982592,
        # 432:15.982592,
        # 433:15.982592,
        # 434:16.023552,
        # 435:16.023552,
        # 436:16.023552,
        # 437:16.023552,
        # 438:16.023552,
        # 439:16.064512,
        # 440:16.35328,
        # 441:16.35328,
        # 442:16.35328,
        # 443:16.35328,
        # 444:16.39424,
        # 445:16.39424,
        # 446:16.39424,
        # 447:16.39424,
        # 448:16.39424,
        # 449:16.4352,
        # 450:16.723968,
        # 451:16.723968,
        # 452:16.723968,
        # 453:16.723968,
        # 454:16.764928,
        # 455:16.764928,
        # 456:16.764928,
        # 457:16.764928,
        # 458:16.764928,
        # 459:16.805888,
        # 460:17.094656,
        # 461:17.094656,
        # 462:17.094656,
        # 463:17.094656,
        # 464:17.135616,
        # 465:17.135616,
        # 466:17.135616,
        # 467:17.135616,
        # 468:17.135616,
        # 469:17.176576,
        # 470:17.465344,
        # 471:17.465344,
        # 472:17.465344,
        # 473:17.465344,
        # 474:17.506304,
        # 475:17.506304,
        # 476:17.506304,
        # 477:17.506304,
        # 478:17.506304,
        # 479:17.547264,
        # 480:17.836032,
        # 481:17.836032,
        # 482:17.836032,
        # 483:17.836032,
        # 484:17.876992,
        # 485:17.876992,
        # 486:17.876992,
        # 487:17.876992,
        # 488:17.876992,
        # 489:17.917952,
        # 490:18.20672,
        # 491:18.20672,
        # 492:18.20672,
        # 493:18.20672,
        # 494:18.24768,
        # 495:18.24768,
        # 496:18.24768,
        # 497:18.24768,
        # 498:18.24768,
        # 499:18.28864,
        # 500:18.577408

    }
    #print TOA
    #print TOA[ack_size]

    if ack_size in TOA:
        #print TOA[ack_size]
        return TOA[ack_size]
    else:
        print 'ERROR IN TOA ' + str(ack_size)
        raw_input('enter to continue')


def bit_to_bytes(bits_results):
    #print 'bit_to_bytes -> ' + str(bits_results)
    bytes_results = defaultdict(float)
    for bit_size in sorted(bits_results):
        #print bit_size
        if bit_size == 0:
            bytes_results[0] += bits_results[bit_size]
        elif bit_size <= 8:
            bytes_results[1] += bits_results[bit_size]        
        elif bit_size <= 16:
            bytes_results[2] += bits_results[bit_size]
        elif bit_size <= 24:
            bytes_results[3] += bits_results[bit_size]        
        elif bit_size <= 32:
            bytes_results[4] += bits_results[bit_size]
        elif bit_size <= 40:
            bytes_results[5] += bits_results[bit_size]        
        elif bit_size <= 48:
            bytes_results[6] += bits_results[bit_size]
        elif bit_size <= 56:
            bytes_results[7] += bits_results[bit_size]        
        elif bit_size <= 64:
            bytes_results[8] += bits_results[bit_size]
        elif bit_size <= 72:
            bytes_results[9] += bits_results[bit_size]        
        elif bit_size <= 80:
            bytes_results[10] += bits_results[bit_size]
        elif bit_size <= 88:
            bytes_results[11] += bits_results[bit_size]        
        elif bit_size <= 96:
            bytes_results[12] += bits_results[bit_size]
        elif bit_size <= 104:
            bytes_results[13] += bits_results[bit_size]        
        elif bit_size <= 112:
            bytes_results[14] += bits_results[bit_size]
        elif bit_size <= 120:
            bytes_results[15] += bits_results[bit_size]        
        elif bit_size <= 128:
            bytes_results[16] += bits_results[bit_size]
        elif bit_size <= 136:
            bytes_results[17] += bits_results[bit_size]
        elif bit_size <= 144:
            bytes_results[18] += bits_results[bit_size]
        elif bit_size <= 152:
            bytes_results[19] += bits_results[bit_size]
        elif bit_size <= 160:
            bytes_results[20] += bits_results[bit_size]
        elif bit_size <= 168:
            bytes_results[21] += bits_results[bit_size]
        elif bit_size <= 176:
            bytes_results[22] += bits_results[bit_size]
        elif bit_size <= 184:
            bytes_results[23] += bits_results[bit_size]
        elif bit_size <= 192:
            bytes_results[24] += bits_results[bit_size]
        elif bit_size <= 200:
            bytes_results[25] += bits_results[bit_size]                                
        elif bit_size <= 208:
            bytes_results[26] += bits_results[bit_size]
        elif bit_size <= 216:
            bytes_results[27] += bits_results[bit_size]
        elif bit_size <= 224:
            bytes_results[28] += bits_results[bit_size]
        elif bit_size <= 232:
            bytes_results[29] += bits_results[bit_size]
        elif bit_size <= 240:
            bytes_results[30] += bits_results[bit_size]
        elif bit_size <= 248:
            bytes_results[31] += bits_results[bit_size]                    
        elif bit_size <= 256:
            bytes_results[32] += bits_results[bit_size]  
        elif bit_size <= 264:
            bytes_results[33] += bits_results[bit_size]  
        elif bit_size <= 272:
            bytes_results[34] += bits_results[bit_size]  
        elif bit_size <= 280:
            bytes_results[35] += bits_results[bit_size]  
        elif bit_size <= 288:
            bytes_results[36] += bits_results[bit_size]  
        elif bit_size <= 296:
            bytes_results[37] += bits_results[bit_size]  
        elif bit_size <= 304:
            bytes_results[38] += bits_results[bit_size]  
        elif bit_size <= 312:
            bytes_results[39] += bits_results[bit_size]  
        elif bit_size <= 320:
            bytes_results[40] += bits_results[bit_size]  
        elif bit_size <= 328:
            bytes_results[41] += bits_results[bit_size]  
        elif bit_size <= 336:
            bytes_results[42] += bits_results[bit_size]  
        elif bit_size <= 344:
            bytes_results[43] += bits_results[bit_size]  
        elif bit_size <= 352:
            bytes_results[44] += bits_results[bit_size]  
        elif bit_size <= 360:
            bytes_results[45] += bits_results[bit_size]  
        elif bit_size <= 368:
            bytes_results[46] += bits_results[bit_size]
        elif bit_size <= 376:
            bytes_results[47] += bits_results[bit_size]
        elif bit_size <= 384:
            bytes_results[48] += bits_results[bit_size]
        elif bit_size <= 392:
            bytes_results[49] += bits_results[bit_size]
        elif bit_size <= 400:
            bytes_results[50] += bits_results[bit_size]
        elif bit_size <= 408:
            bytes_results[51] += bits_results[bit_size]
        elif bit_size <= 416:
            bytes_results[52] += bits_results[bit_size]
        elif bit_size <= 424:
            bytes_results[53] += bits_results[bit_size]
        elif bit_size <= 432:
            bytes_results[54] += bits_results[bit_size]
        elif bit_size <= 440:
            bytes_results[55] += bits_results[bit_size]
        elif bit_size <= 448:
            bytes_results[56] += bits_results[bit_size]    
        elif bit_size <= 456:
            bytes_results[57] += bits_results[bit_size]
        elif bit_size <= 464:
            bytes_results[58] += bits_results[bit_size]
        elif bit_size <= 472:
            bytes_results[59] += bits_results[bit_size]    
        elif bit_size <= 480:
            bytes_results[60] += bits_results[bit_size]
        elif bit_size <= 488:
            bytes_results[61] += bits_results[bit_size]
        elif bit_size <= 496:
            bytes_results[62] += bits_results[bit_size]
        elif bit_size <= 504:
            bytes_results[63] += bits_results[bit_size]
        elif bit_size <= 512:
            bytes_results[64] += bits_results[bit_size]
        
        elif bit_size <= 520:
            bytes_results[65] += bits_results[bit_size]
        elif bit_size <= 528:
            bytes_results[66] += bits_results[bit_size]
        elif bit_size <= 536:
            bytes_results[67] += bits_results[bit_size]
        elif bit_size <= 544:
            bytes_results[68] += bits_results[bit_size]
        elif bit_size <= 576:
            bytes_results[69] += bits_results[bit_size]
        elif bit_size <= 560:
            bytes_results[70] += bits_results[bit_size]                    
        elif bit_size <= 568:
            bytes_results[71] += bits_results[bit_size]
        elif bit_size <= 576:
            bytes_results[72] += bits_results[bit_size]
        elif bit_size <= 584:
            bytes_results[73] += bits_results[bit_size]
        elif bit_size <= 592:
            bytes_results[74] += bits_results[bit_size]
        elif bit_size <= 600:
            bytes_results[75] += bits_results[bit_size]
        elif bit_size <= 608:
            bytes_results[76] += bits_results[bit_size]
        elif bit_size <= 616:
            bytes_results[77] += bits_results[bit_size]
        elif bit_size <= 624:
            bytes_results[78] += bits_results[bit_size]
        elif bit_size <= 632:
            bytes_results[79] += bits_results[bit_size]
        elif bit_size <= 640:
            bytes_results[80] += bits_results[bit_size]    
        else:
            print 'ERROR in bit_to_byte' + str(bit_size)
    #print bytes_results
    return bytes_results