#!/usr/bin/env python3
"""Build a reading-first map page for the Middle East history chapter."""

from __future__ import annotations

import json
import re
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
DATA_PATH = BASE / "data" / "events.json"
HTML_PATH = BASE / "index.html"
READING_MD_PATH = BASE / "docs" / "reading-timeline.md"


CHAPTER_READING = {
    "title": "中东往事第一章：奥斯曼退场与现代中东版图",
    "lead": "这一章最适合按地图读：先看奥斯曼帝国怎样从横跨欧亚非的多民族帝国，逐步退到安纳托利亚；再看英法如何把阿拉伯省份变成委任统治；最后看土耳其和沙特如何从帝国废墟里长成现代国家。",
    "thesis": [
        "现代中东不是古代矛盾自然延续，而是帝国崩溃、欧洲殖民、民族主义、战争和本地王朝竞争共同塑形的结果。",
        "地图上的每一次变化都对应一种权力转移：奥斯曼失去控制，列强取得托管，本地民族运动夺回核心地带，阿拉伯半岛出现新的赢家。",
        "理解这一章的关键，是把条约名和人物名放回地图：谁失去哪块地，谁获得实际控制，谁只得到承诺但没有得到国家。",
    ],
}


DETAILS = {
    "e001": {
        "overview": "1453 年是这一章的起点，因为它解释了奥斯曼为什么能成为近代中东版图的底层结构。君士坦丁堡被攻克后，奥斯曼不只是多了一座城市，而是控制了连接黑海、地中海、巴尔干和安纳托利亚的枢纽。",
        "background": "拜占庭帝国衰落已久，但君士坦丁堡仍有巨大的象征和地缘价值。它是东正教世界的古老中心，也是海峡贸易和军事通道的钥匙。",
        "happened": "奥斯曼把这座城市改造成自己的帝国首都，之后以伊斯坦布尔为中心向欧洲、亚洲和非洲继续扩张。帝国不再只是安纳托利亚的王朝，而成为横跨多个文明区的复合帝国。",
        "map": "地图上要看两块区域：安纳托利亚和巴尔干。君士坦丁堡像一枚铰链，把亚洲部分和欧洲部分扣在一起。",
        "importance": "后面所有问题都从这里展开：奥斯曼越是一个多民族、多宗教、多边疆帝国，近代民族主义和列强干预到来时，裂缝就越多。",
        "takeaways": ["海峡控制是奥斯曼帝国的地缘核心。", "帝国版图不是民族国家，而是多地区、多族群秩序。", "后来的土耳其重生，本质上是在这个帝国核心区收缩后的再建国。"],
    },
    "e002": {
        "overview": "16 世纪的奥斯曼达到强势阶段，控制巴尔干、安纳托利亚、黎凡特、埃及、两河和阿拉伯部分地区。现代中东许多边界问题，都要先理解这个大帝国曾经把这些地区放在同一政治秩序里。",
        "background": "苏莱曼时期的奥斯曼拥有强大的军队、税收体系和宫廷行政，欧洲国家必须把它当成一等强权。它同时面对哈布斯堡、波斯和地中海海权竞争。",
        "happened": "奥斯曼的疆域覆盖今天的土耳其、叙利亚、伊拉克、巴勒斯坦、埃及以及巴尔干大部。这个阶段的帝国不是被动防守，而是主动塑造地区秩序。",
        "map": "地图上应把巴尔干、安纳托利亚、埃及、两河和黎凡特连成一整片看。后面这些区域会一块块从帝国中脱落。",
        "importance": "奥斯曼强盛时的统一空间，解释了为什么一战后中东会突然变成大量新边界：不是本来就小国林立，而是一个大帝国被拆开了。",
        "takeaways": ["16 世纪是理解“帝国原始版图”的基准。", "巴尔干和中东曾在同一帝国秩序中。", "后来的边界变化，本质是这张大图被切开。"],
    },
    "e003": {
        "overview": "1798 年拿破仑远征埃及，是欧洲近代军事和科学体系直接进入奥斯曼边疆的标志。埃及名义上仍属奥斯曼，但实际已经成为英法争夺的战略节点。",
        "background": "埃及控制地中海通往红海和印度洋方向的交通想象。法国想切入英国的东方贸易和印度利益，英国则不能容忍法国控制这条路线。",
        "happened": "法国军队短暂占领埃及，虽然后来撤出，但奥斯曼无法单独处理危机，必须依赖英国等欧洲力量。埃及地方统治者也开始更独立地挑战伊斯坦布尔。",
        "map": "在地图上，埃及不应只看作奥斯曼南部省份，而要看作地中海、红海、印度洋三者之间的锁眼。",
        "importance": "这一事件说明奥斯曼的名义主权和实际控制开始分离。后来的英国占领埃及、苏伊士问题，都从这条线索发展出来。",
        "takeaways": ["埃及成为列强全球战略的一部分。", "奥斯曼开始依赖欧洲力量处理边疆危机。", "名义归属和实际控制分离，是近代中东版图变化的常见模式。"],
    },
    "e004": {
        "overview": "希腊独立是巴尔干民族国家化的开端之一。它把奥斯曼在欧洲的统治问题，从地方叛乱变成欧洲列强共同干预的国际问题。",
        "background": "19 世纪民族主义在欧洲扩散，希腊独立运动得到英法俄不同程度支持。对俄国来说，东正教和南下战略都使它关心巴尔干；对英法来说，不能让俄国单独吃掉奥斯曼遗产。",
        "happened": "希腊最终脱离奥斯曼统治。这个结果鼓励了巴尔干其他民族，也向列强证明：奥斯曼欧洲领土可以被国际会议和军事干预重写。",
        "map": "地图上希腊是第一块明显从奥斯曼欧洲版图中分出去的区域。后来的塞尔维亚、保加利亚、罗马尼亚、黑山会沿类似逻辑继续推进。",
        "importance": "希腊独立不是单独故事，而是巴尔干连锁反应的开端。奥斯曼的欧洲边疆从此越来越难维持。",
        "takeaways": ["民族主义开始改变帝国边界。", "列强干预成为奥斯曼领土问题的常态。", "巴尔干是中东现代史的前奏，不是支线。"],
    },
    "e005": {
        "overview": "坦志麦特改革说明奥斯曼知道自己必须改变，但知道问题并不等于能解决问题。改革试图建立现代行政、法律和军队，却被财政、旧制度和多民族结构同时牵制。",
        "background": "帝国面对欧洲军事压力、债务压力和地方分离倾向。传统军制和地方自治已经无法支撑近代国家竞争，中央必须加强征税、征兵和法律控制。",
        "happened": "改革推动法律平等、军政现代化和中央集权，但这些措施会触动旧贵族、宗教权威、地方势力，也会让各民族开始用新语言要求权利。",
        "map": "这一节点地图边界没有立刻变化，但要看伊斯坦布尔对各省控制力的变化：地图上的线没动，线内部的治理方式在变。",
        "importance": "后面青年土耳其党、凯末尔国家工程，都可以看作改革问题的后续版本：帝国怎样变成现代国家，代价是什么。",
        "takeaways": ["改革是自救，不是装饰。", "中央集权会强化国家，也会激化族群和地方矛盾。", "版图变化有时先发生在治理结构里，再发生在边界线上。"],
    },
    "e006": {
        "overview": "克里米亚战争让奥斯曼暂时保住黑海和海峡安全，却加深了对英法的依赖。它表面上是奥斯曼和俄国的冲突，实质是欧洲列强围绕海峡和东方问题的均势博弈。",
        "background": "俄国长期想南下进入黑海和地中海，奥斯曼挡在通道上。英国和法国不希望俄国单独控制海峡，因此支持奥斯曼。",
        "happened": "英法介入后，俄国被阻止，奥斯曼获得喘息。但战争和改革都需要钱，帝国财政更深地卷入欧洲债务体系。",
        "map": "地图上要看黑海、海峡和安纳托利亚北部。奥斯曼保住的是战略通道，不只是某一块领土。",
        "importance": "奥斯曼的生存越来越依赖列强均势。这样的保护不是免费午餐，后面英法会在奥斯曼衰败时索取回报。",
        "takeaways": ["海峡问题是大国博弈核心。", "英法保护奥斯曼，是为了限制俄国。", "财政依赖会变成政治依赖。"],
    },
    "e007": {
        "overview": "哈米德二世时期是帝国最后的威权续命阶段。他在宪政、情报、宗教合法性和外交平衡之间操作，希望保住帝国，但结构性危机没有消失。",
        "background": "1876 年前后，奥斯曼承受外债、巴尔干危机、俄国压力和内部改革派挑战。宪政被看作救国方案，但苏丹也担心议会和民族政治加速帝国分裂。",
        "happened": "哈米德二世登基后，短暂宪政很快让位于苏丹集权。他试图用泛伊斯兰主义凝聚穆斯林臣民，同时在英法俄德之间保持平衡。",
        "map": "这一节点重点不是边界变化，而是帝国核心如何试图控制边疆。地图上的巴尔干、亚美尼亚、阿拉伯省份都在等待下一轮危机。",
        "importance": "哈米德二世不是单纯反派，他代表帝国在旧秩序中寻找生路。但他的办法也压制了政治参与，给青年土耳其党革命积累动力。",
        "takeaways": ["威权可以拖延危机，却难以解决危机。", "泛伊斯兰主义是帝国凝聚工具。", "青年土耳其党崛起与哈米德统治密切相关。"],
    },
    "e008": {
        "overview": "1878 年柏林会议是奥斯曼欧洲版图的大转折。它确认多个巴尔干国家独立或自治，也让奥匈和英国获得关键利益。",
        "background": "俄土战争后，俄国希望扩大自己在巴尔干的成果，但英奥不愿俄国过度扩张。于是列强把战场结果带到会议桌上重分。",
        "happened": "塞尔维亚、罗马尼亚、黑山独立得到确认，保加利亚自治，波黑由奥匈占领管理，塞浦路斯落入英国控制。奥斯曼名义和实际控制继续分离。",
        "map": "地图上要对照巴尔干、波黑、塞浦路斯。奥斯曼的欧洲空间被切碎，同时英国拿到东地中海据点。",
        "importance": "柏林会议显示中东和巴尔干边界不只由本地战争决定，也由列强会议决定。后来巴黎和会、圣雷莫会议延续了这种逻辑。",
        "takeaways": ["会议桌成为边界制造机器。", "巴尔干民族国家化加速。", "英国和奥匈获得实际战略收益。"],
    },
    "e009": {
        "overview": "1882 年英国占领埃及，是奥斯曼外围殖民化的关键节点。埃及名义上仍与奥斯曼有关，但真正决定埃及命运的是英国的海权和苏伊士利益。",
        "background": "苏伊士运河开通后，埃及成为英国通往印度和东方帝国的生命线。埃及债务和内部政治动荡给英国提供了介入理由。",
        "happened": "英国军事占领埃及，逐步掌握财政、军事和外交方向。奥斯曼没有能力恢复对埃及的实际统治。",
        "map": "地图上埃及要从奥斯曼颜色里淡出，转为英国战略控制区。苏伊士应被看作比开罗更重要的节点。",
        "importance": "这一节点解释了英国为什么在一战后如此关注巴勒斯坦、约旦、伊拉克和阿拉伯半岛：它们都连接埃及、苏伊士和印度洋路线。",
        "takeaways": ["埃及是海权帝国的交通枢纽。", "名义主权不能等同实际控制。", "英国中东政策很大程度围绕苏伊士展开。"],
    },
    "e010": {
        "overview": "亚美尼亚问题是帝国边疆治理失败和民族主义冲突的集中体现。它不只是亚美尼亚人与奥斯曼的关系，也牵涉库尔德人、俄国、欧洲舆论和东安纳托利亚安全。",
        "background": "亚美尼亚人长期生活在奥斯曼东部和高加索之间。俄国南下、欧洲干预和地方土地矛盾，让奥斯曼越来越把亚美尼亚政治诉求视为安全威胁。",
        "happened": "19 世纪末，亚美尼亚问题激化，暴力事件和镇压不断升级。帝国试图用强硬方式处理边疆，但这进一步摧毁族群间信任。",
        "map": "地图上要看东安纳托利亚、高加索和库尔德聚居区的重叠。这里不是一条清楚边界，而是多族群混居的高风险地带。",
        "importance": "一战时期的亚美尼亚灾难不是突然出现的，它有长期边疆冲突、帝国安全焦虑和民族政治背景。",
        "takeaways": ["边疆问题常常是人口、土地和安全问题叠加。", "东安纳托利亚是奥斯曼最敏感的内部裂缝之一。", "地图边界无法完全表达族群混居的复杂性。"],
    },
    "e011": {
        "overview": "青年土耳其党革命把奥斯曼政治带入现代政党、军官集团和民族主义时代。它打着自由宪政旗号，却也推动更强的中央集权。",
        "background": "哈米德二世的威权统治压制改革派和军官集团。萨洛尼卡等地的年轻军官认为，只有恢复宪政和重组国家，帝国才可能避免继续崩溃。",
        "happened": "1908 年革命恢复宪法和议会，青年土耳其党进入权力中心。但掌权后的问题比反对苏丹更难：怎样治理多民族帝国，怎样处理分离主义和列强压力。",
        "map": "地图上可同时高亮巴尔干和安纳托利亚。革命的起点和帝国最脆弱的欧洲边疆紧密相关。",
        "importance": "青年土耳其党既是奥斯曼最后的改革力量，也是之后很多悲剧和战争决策的权力背景。它让帝国从王朝危机转向民族国家危机。",
        "takeaways": ["革命不等于问题解决。", "军官集团成为政治核心。", "中央集权和民族主义开始压过帝国多元秩序。"],
    },
    "e012": {
        "overview": "波黑被奥匈正式兼并，让巴尔干危机从奥斯曼问题转向奥匈与塞尔维亚问题。奥斯曼名义主权继续退场，塞尔维亚民族主义则被进一步刺激。",
        "background": "波黑在 1878 年后由奥匈占领管理，但名义上仍牵涉奥斯曼。1908 年奥匈正式兼并，等于把临时管理变成正式吞并。",
        "happened": "兼并使塞尔维亚追求南斯拉夫或大塞尔维亚目标的情绪上升。俄国暂时无力强硬支持塞尔维亚，但怨恨被保留下来。",
        "map": "地图上波黑从奥斯曼旧体系完全转入奥匈控制。它的位置夹在奥匈、塞尔维亚和巴尔干诸民族之间，是一战前的危险交叉点。",
        "importance": "萨拉热窝事件不是孤立刺杀。波黑兼并让塞尔维亚青年民族主义者有了直接目标。",
        "takeaways": ["波黑是巴尔干火药桶的核心位置。", "奥斯曼退场后，巴尔干并没有稳定。", "奥匈和塞尔维亚的冲突开始取代奥斯曼问题。"],
    },
    "e013": {
        "overview": "1909 年哈米德二世被废黜，意味着奥斯曼最后一位实权苏丹退出舞台。帝国的决策重心从王朝宫廷转向军官、政党和新式官僚。",
        "background": "青年土耳其党革命后，旧势力和新政治之间冲突不断。哈米德试图利用宗教和保守力量反扑，但军官集团掌握了实际武装力量。",
        "happened": "青年土耳其党调兵进入伊斯坦布尔，平息反革命风波，最终废黜哈米德二世。苏丹仍存在，但行政实权大幅削弱。",
        "map": "地图边界不动，但权力中心变了：伊斯坦布尔不再由苏丹个人意志主导，而由军政集团推动帝国最后十几年的选择。",
        "importance": "这为恩维尔、塔拉特、杰马尔等人后来的冒险决策铺路。帝国不是被一个人拖入一战，而是在新权力结构下做出一连串选择。",
        "takeaways": ["苏丹制的实权已经空心化。", "军官政治决定帝国末期走向。", "制度变化会影响战争选择。"],
    },
    "e014": {
        "overview": "意土战争让奥斯曼失去利比亚，也暴露出它已无力保护遥远边疆。欧洲后起列强也能从奥斯曼身上割肉，帝国脆弱性被公开展示。",
        "background": "意大利统一较晚，也想获得殖民地。利比亚距离意大利近、奥斯曼投送能力弱，是最容易下手的目标。",
        "happened": "意大利进攻的黎波里塔尼亚和昔兰尼加，并占领多德卡尼斯群岛。奥斯曼难以通过海路有效增援，只能在压力下停战。",
        "map": "地图上利比亚从奥斯曼北非边疆脱落，多德卡尼斯群岛成为东地中海新的争议点，也牵动希腊和巴尔干局势。",
        "importance": "这场战争像一战预演：海权、殖民野心、奥斯曼投送不足、巴尔干趁机行动，都提前出现。",
        "takeaways": ["奥斯曼已难以保卫海外省份。", "北非和东地中海被欧洲列强切割。", "意土战争给巴尔干战争打开机会窗口。"],
    },
    "e015": {
        "overview": "两次巴尔干战争几乎结束了奥斯曼在欧洲的存在。巴尔干国家先联合赶走奥斯曼，随后又为战利品互相开战。",
        "background": "塞尔维亚、保加利亚、希腊、黑山都想从奥斯曼欧洲领土中获利，但它们的目标互相重叠，尤其是马其顿和萨洛尼卡。",
        "happened": "第一次战争中，巴尔干联盟击败奥斯曼；第二次战争中，保加利亚与前盟友冲突失败。奥斯曼收回部分东色雷斯，但整体已失去绝大多数欧洲领土。",
        "map": "地图上奥斯曼颜色从巴尔干大面积退到伊斯坦布尔附近。塞尔维亚、希腊、保加利亚等版图扩大，阿尔巴尼亚独立。",
        "importance": "这直接制造一战前的巴尔干不稳定：塞尔维亚增强，奥匈更焦虑，民族主义更激烈。",
        "takeaways": ["奥斯曼退出欧洲是现代中东前史。", "巴尔干胜利没有带来和平。", "塞尔维亚增强是萨拉热窝危机的重要背景。"],
    },
    "e016": {
        "overview": "萨拉热窝事件是世界大战的引爆点，但不是根本原因。它把巴尔干民族主义、奥匈安全焦虑、俄德英法同盟体系连接起来。",
        "background": "波黑被奥匈兼并后，塞尔维亚民族主义者认为南斯拉夫人的统一被帝国压制。奥匈则担心塞尔维亚继续鼓动帝国内部斯拉夫人。",
        "happened": "奥匈王储在萨拉热窝被刺杀。奥匈向塞尔维亚施压，德国支持奥匈，俄国支持塞尔维亚，法国、英国相继卷入。",
        "map": "地图上先看萨拉热窝，再向外扩散到欧洲同盟网络。奥斯曼还没有立即成为主战场，但它很快会被拖入。",
        "importance": "一战改变了中东，因为奥斯曼站到了失败的一边。没有这场大战，英法无法用战胜国身份重画阿拉伯省份。",
        "takeaways": ["刺杀是导火索，不是全部原因。", "巴尔干危机升级为全球战争。", "中东版图变化从欧洲战争开始。"],
    },
    "e017": {
        "overview": "奥斯曼倒向德国，是帝国末期最关键的战略选择之一。它不是完全被迫，但决策者高估德国、低估战争消耗，也误判了英法俄对奥斯曼遗产的野心。",
        "background": "青年土耳其党中的恩维尔帕夏崇拜德国军事力量。英国扣押奥斯曼订购的无畏舰，进一步刺激反英情绪；德国军舰事件也推动奥斯曼靠向同盟国。",
        "happened": "奥斯曼与德国秘密结盟，之后逐步参战。它希望借德国力量对抗俄国并收复失地，却把自己带入无法承受的总体战。",
        "map": "地图上应把奥斯曼放在德国、俄国、英国之间看。它的地理位置可以威胁海峡、苏伊士、高加索和波斯湾，因此一参战就变成多线战场。",
        "importance": "这个选择决定了战后清算。英法不再只是蚕食边疆，而会以战胜国身份处理整个帝国。",
        "takeaways": ["奥斯曼参战是战略赌博。", "英国扣舰强化亲德路线。", "失败一方身份决定了战后被分割命运。"],
    },
    "e018": {
        "overview": "1915 年同时有加里波利和亚美尼亚灾难两条线。前者让凯末尔崭露头角，后者则显示帝国在总体战压力下如何把边疆安全问题转化为族群暴力。",
        "background": "协约国想通过达达尼尔海峡打通补给俄国的通道，奥斯曼则担心东部亚美尼亚人与俄国合作。战争把所有不信任都放大。",
        "happened": "奥斯曼在加里波利挡住协约国登陆；同时对亚美尼亚人实施强制迁徙和屠杀，造成巨大人道灾难。",
        "map": "地图上要同时看达达尼尔海峡和东安纳托利亚。一个是军事防御点，一个是人口版图被暴力改变的边疆。",
        "importance": "这解释了土耳其民族国家形成时的人口背景，也解释亚美尼亚问题为什么至今仍是历史记忆和国际政治争议。",
        "takeaways": ["加里波利提升了凯末尔声望。", "东安纳托利亚人口版图被暴力重塑。", "战争压力会把安全恐惧推向极端政策。"],
    },
    "e019": {
        "overview": "英国与伊本沙特建立战时关系，是阿拉伯半岛后续格局的伏笔。英国不是只押注哈希姆家族，也在内志寻找能牵制奥斯曼和稳定半岛的力量。",
        "background": "阿拉伯半岛内部存在哈希姆家族、沙特家族、拉希德家族等竞争。英国的目标是战时削弱奥斯曼，并维护波斯湾、印度洋和苏伊士路线安全。",
        "happened": "英国与伊本沙特达成关系，给予承认和补贴。伊本沙特暂时不是英国最亮眼的伙伴，但他在内志的组织能力和军事扩张潜力不断增强。",
        "map": "地图上要区分汉志和内志。哈希姆家族控制圣地汉志，沙特家族的核心在内志，两者最终会争夺阿拉伯半岛中心地位。",
        "importance": "这条线解释了为什么一战后不是哈希姆统一阿拉伯，而是沙特最终控制麦加、麦地那并建立王国。",
        "takeaways": ["英国同时经营多个阿拉伯伙伴。", "内志和汉志不是同一个政治空间。", "沙特崛起的外部条件在一战时形成。"],
    },
    "e020": {
        "overview": "麦克马洪-侯赛因通信让阿拉伯独立看似近在眼前，却从一开始就存在边界歧义。英国需要阿拉伯起义，但不愿放弃与法国和自身帝国路线的安排。",
        "background": "麦加谢里夫侯赛因希望借战争建立阿拉伯王国。英国希望阿拉伯人反抗奥斯曼，减少自己在中东战场的成本。",
        "happened": "双方通信中谈到阿拉伯独立范围，但对叙利亚、巴勒斯坦、伊拉克等地的解释并不一致。承诺留下大量模糊地带。",
        "map": "地图上可用虚线框出阿拉伯独立想象范围，再叠加后来的英法分割线，就能看出承诺之间的冲突。",
        "importance": "阿拉伯世界对西方背叛感的重要来源之一，就是这种战时承诺和战后现实的落差。",
        "takeaways": ["阿拉伯独立承诺从一开始就不清晰。", "英国用模糊语言换取战时合作。", "后来的委任统治与这份承诺直接冲突。"],
    },
    "e021": {
        "overview": "赛克斯-皮科协定是英法秘密分割奥斯曼阿拉伯省份的核心文本。它让阿拉伯独立承诺和欧洲帝国安排正面冲突。",
        "background": "英法都预判奥斯曼会战败，于是提前规划战后势力范围。法国重视叙利亚和黎巴嫩，英国重视伊拉克、波斯湾、巴勒斯坦和通往印度的路线。",
        "happened": "协定把叙利亚、伊拉克、巴勒斯坦等地划入不同势力范围或国际安排。它并非今天所有边界的唯一来源，但代表了列强瓜分逻辑。",
        "map": "地图上要叠加两层：阿拉伯起义想象的统一空间，以及英法划出的势力范围。两层越重叠，冲突越明显。",
        "importance": "它解释了现代中东很多政治叙事中的核心怨念：当地人参战换来的不是统一独立，而是外部托管和分割。",
        "takeaways": ["英法提前规划战后分割。", "叙利亚、伊拉克、巴勒斯坦进入列强安排。", "赛克斯-皮科象征承诺破裂。"],
    },
    "e022": {
        "overview": "阿拉伯起义削弱了奥斯曼在汉志和叙利亚方向的控制，也让哈希姆家族成为英国中东方案的重要棋子。",
        "background": "侯赛因和他的儿子们希望用起义换取战后阿拉伯王国。英国则看重它对奥斯曼铁路、驻军和后方稳定的打击。",
        "happened": "起义军在劳伦斯等英国人员配合下攻击汉志铁路，逐步向北推进。它的军事规模有限，但政治象征很强。",
        "map": "地图上要沿汉志铁路从麦加、麦地那方向看向大马士革。起义不是整个阿拉伯世界同时起身，而是一条从汉志向叙利亚推进的战线。",
        "importance": "起义创造了哈希姆家族战后索取王位的资本，也为费萨尔进入大马士革埋下伏笔。",
        "takeaways": ["阿拉伯起义是军事行动，也是政治投资。", "汉志铁路是关键目标。", "起义成果后来被英法重新分配。"],
    },
    "e023": {
        "overview": "贝尔福宣言和耶路撒冷陷落，把巴勒斯坦问题推入现代中东版图核心。英国一边处理阿拉伯承诺，一边支持犹太民族家园，承诺结构进一步复杂化。",
        "background": "巴勒斯坦在奥斯曼时期不是现代意义的民族国家边界单元，但它有宗教圣地、战略通道和帝国政治价值。英国占领耶路撒冷后，实际控制开始改变。",
        "happened": "英国发表贝尔福宣言，支持犹太人在巴勒斯坦建立民族家园；同年英军占领耶路撒冷，结束奥斯曼对这座圣城数百年的统治。",
        "map": "地图上巴勒斯坦很小，但意义极大。它连接埃及、叙利亚、约旦和地中海，也连接三大宗教记忆。",
        "importance": "这一节点解释了为什么巴勒斯坦问题不是战后才突然出现，而是在一战期间就被英国承诺和军事占领共同塑造。",
        "takeaways": ["巴勒斯坦进入英国战后安排核心。", "贝尔福宣言与阿拉伯承诺互相冲突。", "耶路撒冷的象征价值远大于面积。"],
    },
    "e024": {
        "overview": "1918 年大马士革易手和奥斯曼停战，标志着奥斯曼在阿拉伯世界的统治基本结束。接下来真正的问题是：谁来接管这些省份。",
        "background": "一战后期，奥斯曼多线作战、资源枯竭。英军和阿拉伯起义军在叙利亚方向推进，德国和奥匈也相继走向失败。",
        "happened": "费萨尔部队和英军进入大马士革，奥斯曼签署停战。阿拉伯人期待独立，但英法早已有自己的战后安排。",
        "map": "地图上奥斯曼色块应从叙利亚、伊拉克、巴勒斯坦和阿拉伯半岛淡出。这里从帝国省份变成战胜国处理对象。",
        "importance": "这是一战前后中东版图的真正断点：奥斯曼退场后，阿拉伯世界并没有自动统一，而是进入委任统治和王朝安置阶段。",
        "takeaways": ["奥斯曼阿拉伯省份统治结束。", "大马士革成为阿拉伯独立想象的中心。", "战后接管权落入英法手中。"],
    },
    "e025": {
        "overview": "巴黎和会与希腊登陆士麦那，把战后分割压力推到奥斯曼核心区。安纳托利亚不再只是失去外围，而面临本土被拆分的风险。",
        "background": "协约国战胜后处理奥斯曼遗产。希腊追求“大希腊”理想，想把安纳托利亚西岸和爱琴海希腊人聚居区纳入版图。",
        "happened": "希腊军队在士麦那登陆，协约国讨论对奥斯曼的严厉安排。凯末尔由此获得组织民族抵抗的历史机会。",
        "map": "地图上要看安纳托利亚西岸、海峡和东部亚美尼亚方案。奥斯曼不仅失去阿拉伯地区，连核心家底也被摆上谈判桌。",
        "importance": "凯末尔的合法性来自这种危机：如果不反抗，安纳托利亚也会被分割。土耳其民族运动因此不是复辟奥斯曼，而是保住核心领土。",
        "takeaways": ["战后分割触及安纳托利亚核心。", "希腊登陆激发土耳其民族抵抗。", "巴黎和会让列强分赃逻辑公开化。"],
    },
    "e026": {
        "overview": "1920 年圣雷莫和塞夫尔方案，是现代中东边界草稿最密集出现的阶段。阿拉伯省份被委任统治化，安纳托利亚也被设计成分割对象。",
        "background": "协约国需要把战时承诺、军事占领、石油利益、法国叙利亚诉求、英国伊拉克和巴勒斯坦诉求合并成战后秩序。",
        "happened": "法国获得叙利亚和黎巴嫩委任统治，英国获得伊拉克和巴勒斯坦委任统治。塞夫尔条约还设想希腊、亚美尼亚、库尔德和海峡国际化安排。",
        "map": "地图上最重要的是分层看：阿拉伯地区由英法托管，安纳托利亚核心区被多个方案切割。它是一张没有真正落地的极限分割图。",
        "importance": "塞夫尔之所以重要，不是因为它最终成功，而是因为它刺激了土耳其民族运动，并展示战胜国本来想怎样处理奥斯曼。",
        "takeaways": ["委任统治把阿拉伯省份制度化分割。", "塞夫尔方案威胁安纳托利亚核心。", "1920 是战后中东边界设计的关键年。"],
    },
    "e027": {
        "overview": "费萨尔的叙利亚王国失败，说明阿拉伯统一理想抵不过法国委任统治和英法战后安排。大马士革的短暂独立梦被迅速击碎。",
        "background": "费萨尔凭借阿拉伯起义和进入大马士革的资本，试图建立叙利亚王国。但法国认为叙利亚和黎巴嫩属于自己的势力范围。",
        "happened": "法国军事击败费萨尔，驱逐其政权。英国不愿为了费萨尔与法国决裂，于是转而把费萨尔安置到伊拉克。",
        "map": "地图上大叙利亚被法国委任统治覆盖，费萨尔从大马士革离场。哈希姆家族的政治空间从叙利亚转向伊拉克和外约旦。",
        "importance": "这是阿拉伯统一失败的关键节点。之后的阿拉伯国家边界，不再以大叙利亚或统一王国为中心，而以英法托管区为基础。",
        "takeaways": ["费萨尔失去叙利亚。", "法国委任统治压过阿拉伯独立。", "哈希姆家族被英国重新安置。"],
    },
    "e028": {
        "overview": "开罗会议是英国中东 B 计划的核心：既然统一阿拉伯王国做不成，就用哈希姆家族分别安置伊拉克和外约旦，同时保留巴勒斯坦安排。",
        "background": "英国战后面对成本问题、伊拉克反抗、法国控制叙利亚、阿拉伯承诺压力以及巴勒斯坦问题。丘吉尔和劳伦斯等人试图用较低成本稳定局面。",
        "happened": "费萨尔被安排为伊拉克国王，阿卜杜拉进入外约旦，巴勒斯坦单独保留在英国安排内。哈希姆家族得到王位，但没有得到统一阿拉伯。",
        "map": "地图上应把伊拉克、外约旦、巴勒斯坦拆开看。它们不是自然生成的古老边界，而是英国在委任统治框架中的管理方案。",
        "importance": "今天约旦、伊拉克早期王国和巴勒斯坦问题，都能在这个节点看到制度来源。",
        "takeaways": ["英国用王室安置替代阿拉伯统一。", "伊拉克、外约旦、巴勒斯坦被分开管理。", "开罗会议是现代阿拉伯东部版图的重要节点。"],
    },
    "e029": {
        "overview": "土耳其民族运动击败希腊，是塞夫尔方案破产的军事基础。凯末尔证明安纳托利亚不是战胜国可以随意切割的空白地图。",
        "background": "希腊军队深入安纳托利亚，协约国希望用希腊力量执行部分战后安排。土耳其民族运动则以安卡拉为中心组织抵抗。",
        "happened": "土耳其军队击败希腊，重新控制安纳托利亚西部。希腊的大希腊方案破产，协约国不得不重新谈判。",
        "map": "地图上看士麦那和安纳托利亚西部。希腊势力从内陆被推出，土耳其民族运动的控制范围扩大。",
        "importance": "没有军事胜利，就没有后来的洛桑条约。土耳其边界是打出来再谈出来的，不是协约国主动赠送的。",
        "takeaways": ["塞夫尔方案在战场上失效。", "凯末尔民族运动取得决定性资本。", "现代土耳其边界开始成形。"],
    },
    "e030": {
        "overview": "苏丹制废除，标志奥斯曼王朝政治实体走向终结。土耳其民族运动不是抢救旧帝国，而是在废墟中建立新共和国。",
        "background": "安卡拉政府和伊斯坦布尔苏丹政府之间存在合法性竞争。民族运动胜利后，继续保留苏丹会妨碍新国家建构。",
        "happened": "土耳其大国民议会废除苏丹制，王朝权威退出政治中心。共和国还未正式宣布，但旧帝国外壳已经被拆掉。",
        "map": "地图边界变化不大，但政治符号变化巨大：伊斯坦布尔王朝中心让位于安卡拉民族国家中心。",
        "importance": "这解释了土耳其和奥斯曼的关系：现代土耳其继承核心地理，却主动切断王朝帝国的政治形式。",
        "takeaways": ["奥斯曼王朝退出政治舞台。", "安卡拉成为新合法性中心。", "土耳其重生不是奥斯曼复辟。"],
    },
    "e031": {
        "overview": "洛桑条约取代塞夫尔条约，现代土耳其边界基本确立。土耳其保住安纳托利亚和东色雷斯，但也接受放弃阿拉伯帝国部分。",
        "background": "土耳其民族运动取得军事胜利后，协约国必须重新谈判。塞夫尔条约太严厉且无法执行，洛桑成为现实妥协。",
        "happened": "洛桑确认土耳其主权和边界，独立亚美尼亚、库尔德国家和希腊深入安纳托利亚的方案退出正式安排。人口交换也改变了希土两国社会结构。",
        "map": "地图上土耳其边界收缩但稳固：核心是安纳托利亚加东色雷斯。叙利亚、伊拉克、巴勒斯坦等阿拉伯省份不再回来。",
        "importance": "洛桑是土耳其国家成功的节点，也是奥斯曼帝国正式终结后的现实边界确认。",
        "takeaways": ["现代土耳其边界在洛桑后稳定。", "塞夫尔的极限分割被推翻。", "土耳其保核心，失帝国。"],
    },
    "e032": {
        "overview": "哈里发制废除后，侯赛因试图争夺伊斯兰世界象征权威，但这一步反而加速了他与英国、沙特之间的裂痕。",
        "background": "奥斯曼苏丹长期兼具哈里发象征。凯末尔废除哈里发制后，麦加谢里夫侯赛因认为自己有资格接过宗教政治权威。",
        "happened": "侯赛因宣布哈里发，但英国并不愿支持他扩大权威。伊本沙特则把这视为挑战，向汉志推进。",
        "map": "地图上看土耳其和汉志的联系断裂。哈里发象征从伊斯坦布尔消失，圣地所在的汉志成为新的争夺焦点。",
        "importance": "这解释了为什么哈希姆家族失去汉志：它在象征政治上走得太远，却缺少足够军事和外部支持。",
        "takeaways": ["哈里发制废除改变伊斯兰政治象征。", "侯赛因的野心超过英国可接受范围。", "汉志危机直接引向沙特扩张。"],
    },
    "e033": {
        "overview": "沙特夺取汉志，是阿拉伯半岛权力结构的决定性翻转。控制麦加、麦地那和吉达后，伊本沙特不再只是内志地方强人。",
        "background": "哈希姆家族依靠圣地地位和英国关系，长期控制汉志；沙特家族则从内志扩张，拥有更强的军事组织和宗教动员能力。",
        "happened": "伊本沙特进攻汉志，侯赛因失去麦加、麦地那、吉达等关键城市。哈希姆家族退出阿拉伯半岛核心，只在英国安排下保留约旦和当时伊拉克王位。",
        "map": "地图上汉志从哈希姆控制转入沙特控制。阿拉伯半岛西部圣地和中部内志被连起来。",
        "importance": "这一步让后来的沙特阿拉伯拥有宗教圣地和半岛腹地，改变整个阿拉伯世界的政治重心。",
        "takeaways": ["汉志是圣地，也是战略海岸。", "沙特击败哈希姆家族。", "现代沙特王国的关键拼图完成。"],
    },
    "e034": {
        "overview": "1932 年沙特阿拉伯王国成立，标志阿拉伯半岛中西部被新王国整合。第一章至此完成从奥斯曼帝国到现代中东国家体系的主要转场。",
        "background": "伊本沙特已经控制内志、汉志和周边地区，需要把征服结果制度化为国家。英国也逐渐接受沙特作为半岛稳定力量。",
        "happened": "沙特阿拉伯王国成立，沙特家族把内陆部落联盟、宗教合法性和圣地控制结合成新的国家结构。",
        "map": "地图上阿拉伯半岛中部和西部连成一体。哈希姆家族的阿拉伯统一梦结束，沙特成为半岛最大赢家。",
        "importance": "这不是奥斯曼直接遗产，而是一战后权力真空、本地王朝竞争和英国策略共同塑造的新结果。",
        "takeaways": ["沙特王国是奥斯曼退场后的新国家。", "圣地控制提升沙特地位。", "第一章的终点是现代中东底图初步成形。"],
    },
}


PHASE_CONTEXT = {
    "帝国高峰": "这一阶段的重点，是看海峡、安纳托利亚、巴尔干和阿拉伯省份怎样被装进同一套帝国秩序。",
    "改革与债务": "这一阶段的重点，是看改革怎样补救落后，又怎样被债务、贷款和地方分离牵住手脚。",
    "巴尔干脱离": "这一阶段的重点，是看奥斯曼欧洲领土怎样被民族主义和列强会议一块块改写。",
    "外围被切割": "这一阶段的重点，是看列强怎样先拿走帝国边缘和战略通道，再影响帝国核心。",
    "民族问题": "这一阶段的重点，是看内部族群政治怎样从治理问题变成安全问题。",
    "青年土耳其党": "这一阶段的重点，是看立宪、军人政治和土耳其民族主义如何替代旧式苏丹权威。",
    "一战": "这一阶段的重点，是看奥斯曼如何在高加索、海峡、阿拉伯半岛和巴勒斯坦同时承压。",
    "阿拉伯方案": "这一阶段的重点，是看阿拉伯政治想象如何被英国战时承诺激活，又怎样被战后分配压缩。",
    "英法分割": "这一阶段的重点，是看英法如何把奥斯曼阿拉伯省份转化为势力范围和委任统治地。",
    "一战结束": "这一阶段的重点，是看军事停战以后，占领城市、港口和行政机关如何变成谈判筹码。",
    "战后分割": "这一阶段的重点，是看巴黎、圣雷莫、塞夫尔等会议如何把战时承诺制度化。",
    "土耳其重生": "这一阶段的重点，是看安纳托利亚如何从战败帝国残余地带，变成土耳其民族国家核心。",
    "沙特崛起": "这一阶段的重点，是看阿拉伯半岛在奥斯曼退场和英国间接影响下重新洗牌。",
}


def suggested_layer_label(event: dict) -> str:
    year = int(float(event["year"]))
    if year < 1500:
        return "1500 奥斯曼早期扩张"
    if 1500 <= year < 1700:
        return "1600 奥斯曼高峰"
    if 1878 <= year < 1912:
        return "1878 柏林会议后"
    if 1912 <= year < 1920:
        return "1913 巴尔干战争后"
    if 1920 <= year < 1923:
        return "1920 委任统治/塞夫尔"
    if year >= 1923:
        return "1923 洛桑后"
    return "早期近代过渡阶段，当前没有精确同年边界层"


def strip_sentence_end(text: str) -> str:
    return text.rstrip("。；;.!！")


def build_lecture(event: dict, previous_event: dict | None, next_event: dict | None) -> str:
    detail = event["reading"]
    actors = "、".join(event.get("actors") or [])
    takeaways = "；".join(strip_sentence_end(item) for item in detail["takeaways"])
    previous_text = (
        f"它承接的是前一个节点“{previous_event['title']}”留下的问题。"
        if previous_event
        else "它是整章的入口，需要先建立一个坐标：现代中东边界是从奥斯曼帝国这个大框架里逐步分解出来的。"
    )
    next_text = (
        f"往后看，它会把问题推向“{next_event['title']}”。"
        if next_event
        else "到这里，第一章的版图主线基本收束：旧帝国退场，现代国家和委任统治体系成为新的背景。"
    )
    phase_context = PHASE_CONTEXT.get(
        event["phase"],
        "这一阶段要把事件放回帝国、列强和地方政治三者之间看，地图上的线只是结果。",
    )
    return "\n\n".join(
        [
            f"这一节要读的不是孤立年份，而是“{event['phase']}”阶段里的一次结构性转折。{detail['overview']} {previous_text} {phase_context}",
            f"先看背景。{detail['background']} 参与者主要包括{actors}。他们关注的并不只是某一座城市或某一条边界，而是谁有权征税、驻军、任命官员、控制交通线，以及谁能代表当地人向国际社会说话。历史事件常常先表现为人物和口号，真正落到地图上时才变成边界、托管、占领区或自治区域。",
            f"再看事情本身。{detail['happened']} 如果把它放进整章叙事，它的含义是：{event['summary']} 这类变化通常不会只改变一个地方，它会让周边势力重新计算成本和机会。帝国中央会担心连锁效应，地方精英会寻找新的保护人，外部力量也会判断自己能否借机扩大影响。",
            f"地图上要读得更慢。{detail['map']} 本节点对应的版图变化可以概括为：{event['territory_change']} 你在左侧地图上应先找到{event['regions_label']}，再看这些区域和海峡、地中海、红海、两河流域或阿拉伯半岛的关系。当前最适合显示的历史层是“{suggested_layer_label(event)}”。如果边界线没有立刻移动，也不要跳过地图，因为行政控制、军事通道、港口和圣地的变化，往往会在几年后才以正式条约的形式显现出来。",
            f"最后看它为什么重要。{detail['importance']} 可以把这一节记成三句话：{takeaways}。{next_text} 这样读下来，时间线就不只是事件列表，而是一条版图收缩和权力转移的链：奥斯曼逐渐失去外围，列强把战略地带制度化，本地民族运动和王朝力量再把其中一部分重新组织成现代国家。",
        ]
    )


def enrich(payload: dict) -> dict:
    events = payload["events"]
    for index, event in enumerate(events):
        event["reading"] = DETAILS[event["id"]]
        event["reading"]["lecture"] = build_lecture(
            event,
            events[index - 1] if index else None,
            events[index + 1] if index + 1 < len(events) else None,
        )
    payload["chapter_reading"] = CHAPTER_READING
    payload["episode_transcripts"] = build_episode_transcripts() or payload.get("episode_transcripts", {})
    return payload


def build_episode_transcripts() -> dict:
    transcripts = {}
    for path in sorted((BASE / "transcripts").glob("*.srt")):
        match = re.match(r"^(1\.\d+)\s", path.stem)
        episode = match.group(1) if match else "summary"
        chunks = []
        current_chunk = None
        for block in re.split(r"\n\s*\n", path.read_text(encoding="utf-8-sig").strip()):
            lines = block.splitlines()
            if len(lines) < 3 or " --> " not in lines[1]:
                continue
            timestamp = lines[1].split(" --> ", 1)[0]
            hours, minutes, seconds = timestamp.replace(",", ".").split(":")
            start = int(hours) * 3600000 + int(minutes) * 60000 + round(float(seconds) * 1000)
            text = "".join(lines[2:]).strip()
            if not text:
                continue
            if current_chunk is None or start - current_chunk["start_ms"] >= 60000 or len(current_chunk["text"]) >= 500:
                current_chunk = {"start_ms": start, "time": timestamp.split(",", 1)[0], "text": ""}
                chunks.append(current_chunk)
            current_chunk["text"] += text
        if chunks:
            transcripts[episode] = {"title": path.stem, "chunks": chunks, "characters": sum(len(chunk["text"]) for chunk in chunks)}
    return transcripts


def build_reading_markdown(payload: dict) -> str:
    lines = [
        "# 中东往事第一章：阅读型时间线",
        "",
        CHAPTER_READING["lead"],
        "",
        "## 主线",
        "",
    ]
    for item in CHAPTER_READING["thesis"]:
        lines.append(f"- {item}")
    lines.append("")
    for event in payload["events"]:
        detail = event["reading"]
        lines.extend(
            [
                f"## {event['date']}｜{event['title']}",
                "",
                "### 长文讲义",
                "",
                detail["lecture"],
                "",
                "### 快速索引",
                "",
                detail["overview"],
                "",
                f"### 背景\n\n{detail['background']}",
                "",
                f"### 发生了什么\n\n{detail['happened']}",
                "",
                f"### 地图怎么读\n\n{detail['map']}",
                "",
                f"### 为什么重要\n\n{detail['importance']}",
                "",
                "### 记住这几点",
                "",
            ]
        )
        for takeaway in detail["takeaways"]:
            lines.append(f"- {takeaway}")
        lines.append("")
    return "\n".join(lines)


def build_html(payload: dict) -> str:
    data = json.dumps(payload, ensure_ascii=False, indent=2)
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <link rel="icon" href="data:," />
  <title>中东往事第一章 - 长文地图阅读版</title>
  <style>
    :root {{
      color-scheme: light;
      --paper: #f4efe4;
      --ink: #17212b;
      --muted: #69737d;
      --line: #d8cdbf;
      --panel: #fffaf1;
      --accent: #b85c38;
      --sea: #d7e7e5;
      --land: #ebe0cd;
      --country: #c9baa4;
      --teal: #2f8f83;
      --shadow: 0 10px 28px rgba(34, 31, 27, 0.1);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--paper);
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Noto Sans CJK SC", "Microsoft YaHei", Arial, sans-serif;
      letter-spacing: 0;
    }}
    header {{
      padding: 22px clamp(16px, 3vw, 34px) 12px;
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 18px;
      align-items: end;
    }}
    h1 {{
      margin: 0;
      font-size: clamp(25px, 3vw, 42px);
      line-height: 1.1;
      max-width: 1040px;
    }}
    .subhead {{
      margin: 8px 0 0;
      color: var(--muted);
      font-size: 15px;
      line-height: 1.65;
      max-width: 1080px;
    }}
    .source-badge {{
      border: 1px solid var(--line);
      background: rgba(255, 250, 241, 0.78);
      padding: 10px 12px;
      border-radius: 8px;
      font-size: 13px;
      color: var(--muted);
      min-width: 220px;
      text-align: right;
    }}
    main {{
      padding: 8px clamp(16px, 3vw, 34px) 32px;
      display: grid;
      grid-template-columns: minmax(420px, 0.9fr) minmax(460px, 1.1fr);
      gap: 18px;
      align-items: start;
    }}
    .map-column {{
      position: sticky;
      top: 12px;
      display: grid;
      gap: 12px;
    }}
    .controls, .map-wrap, .reader, .timeline {{
      border: 1px solid var(--line);
      background: var(--panel);
      border-radius: 8px;
      box-shadow: var(--shadow);
    }}
    .controls {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      padding: 12px;
    }}
    .controls input[type="range"] {{
      grid-column: 1 / -1;
      width: 100%;
      accent-color: var(--accent);
    }}
    .control-field {{
      display: grid;
      gap: 5px;
    }}
    .control-label {{
      color: var(--muted);
      font-size: 12px;
      font-weight: 800;
      line-height: 1;
    }}
    select, button {{
      height: 38px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fffdf7;
      color: var(--ink);
      padding: 0 10px;
      font: inherit;
    }}
    button {{
      cursor: pointer;
      font-weight: 800;
    }}
    .button-row {{
      grid-column: 1 / -1;
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 8px;
    }}
    .play {{
      background: #17212b;
      color: #fffaf1;
    }}
    .map-wrap {{
      padding: 12px;
      display: grid;
      gap: 10px;
      position: relative;
    }}
    svg {{
      width: 100%;
      height: min(58vh, 610px);
      min-height: 390px;
      border-radius: 6px;
      background: var(--sea);
      border: 1px solid #cbdcd8;
    }}
    .country {{
      fill: var(--land);
      stroke: var(--country);
      stroke-width: 1.1;
      vector-effect: non-scaling-stroke;
    }}
    .historical-country {{
      fill: rgba(184, 92, 56, 0.16);
      stroke: rgba(75, 55, 42, 0.72);
      stroke-width: 1.25;
      vector-effect: non-scaling-stroke;
    }}
    .historical-country.precision-low {{
      stroke-dasharray: 5 4;
      fill: rgba(128, 98, 168, 0.13);
    }}
    .historical-country.ottoman-core {{
      fill: rgba(198, 54, 34, 0.64);
      stroke: #5b1712;
      stroke-width: 2.35;
      stroke-dasharray: none;
      filter: drop-shadow(0 2px 3px rgba(92, 25, 18, 0.28));
    }}
    .historical-country.ottoman-dependent {{
      fill: rgba(242, 181, 73, 0.32);
      stroke: rgba(122, 78, 18, 0.95);
      stroke-width: 1.75;
      stroke-dasharray: 8 4;
    }}
    .historical-country.ottoman-core.precision-low {{
      stroke-dasharray: none;
    }}
    .historical-country.ottoman-dependent.precision-low {{
      stroke-dasharray: 8 4;
    }}
    .region {{
      opacity: 0.12;
      stroke: rgba(31, 34, 36, 0.22);
      stroke-width: 1.2;
      vector-effect: non-scaling-stroke;
      transition: opacity 180ms ease, filter 180ms ease, stroke-width 180ms ease;
    }}
    .region.active {{
      opacity: 0.72;
      stroke: #1d1712;
      stroke-width: 2.3;
      filter: drop-shadow(0 5px 5px rgba(30, 25, 20, 0.22));
    }}
    .graticule {{
      fill: none;
      stroke: rgba(75, 92, 101, 0.18);
      stroke-width: 0.8;
      vector-effect: non-scaling-stroke;
    }}
    .label {{
      font-size: 12px;
      font-weight: 800;
      fill: rgba(23, 33, 43, 0.65);
      paint-order: stroke;
      stroke: rgba(255, 250, 241, 0.85);
      stroke-width: 3px;
      pointer-events: none;
    }}
    .marker {{
      fill: rgba(23, 33, 43, 0.22);
      stroke: rgba(23, 33, 43, 0.42);
      stroke-width: 1.4;
      vector-effect: non-scaling-stroke;
      cursor: pointer;
    }}
    .marker.past {{ fill: rgba(184, 92, 56, 0.38); stroke: rgba(184, 92, 56, 0.78); }}
    .marker.current {{ fill: #17212b; stroke: #fffaf1; stroke-width: 3; }}
    .legend {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px 14px;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.4;
    }}
    .legend span {{ display: inline-flex; align-items: center; gap: 6px; }}
    .swatch {{
      width: 13px;
      height: 13px;
      border-radius: 3px;
      display: inline-block;
      border: 1px solid rgba(23, 33, 43, 0.25);
    }}
    .reader {{
      overflow: hidden;
    }}
    .chapter {{
      padding: 18px 20px;
      border-bottom: 1px solid var(--line);
      background: rgba(255, 253, 247, 0.72);
    }}
    .chapter h2, .detail h2 {{
      margin: 0 0 10px;
      font-size: 25px;
      line-height: 1.18;
    }}
    .chapter p, .detail p {{
      margin: 10px 0;
      color: #26313b;
      line-height: 1.72;
      font-size: 15.5px;
    }}
    .thesis {{
      display: grid;
      gap: 8px;
      margin-top: 12px;
    }}
    .thesis div {{
      border-left: 3px solid var(--teal);
      padding: 8px 10px;
      background: rgba(47, 143, 131, 0.07);
      line-height: 1.6;
      color: #26313b;
    }}
    .detail {{
      padding: 20px;
    }}
    .kicker {{
      color: var(--accent);
      font-weight: 800;
      font-size: 14px;
      margin-bottom: 6px;
    }}
    .section {{
      margin-top: 18px;
      padding-top: 14px;
      border-top: 1px solid rgba(216, 205, 191, 0.78);
    }}
    .lecture {{
      display: grid;
      gap: 14px;
      margin-top: 14px;
    }}
    .lecture p {{
      margin: 0;
      font-size: 16.5px;
      line-height: 1.9;
      color: #1f2a33;
    }}
    .quick-index {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
    }}
    .section h3 {{
      margin: 0 0 8px;
      font-size: 16px;
      line-height: 1.35;
    }}
    .takeaways {{
      display: grid;
      gap: 8px;
      padding: 0;
      margin: 10px 0 0;
      list-style: none;
    }}
    .takeaways li {{
      padding: 8px 10px;
      border-left: 3px solid var(--accent);
      background: rgba(184, 92, 56, 0.07);
      line-height: 1.55;
    }}
    .meta {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 12px;
    }}
    .chip {{
      border: 1px solid var(--line);
      border-radius: 999px;
      padding: 5px 9px;
      color: var(--muted);
      background: #fffdf7;
      font-size: 12px;
      max-width: 100%;
    }}
    .timeline {{
      overflow: hidden;
      display: grid;
      grid-template-rows: auto 1fr;
      max-height: 430px;
    }}
    .timeline-head {{
      padding: 12px 14px;
      border-bottom: 1px solid var(--line);
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: center;
      color: var(--muted);
      font-size: 13px;
    }}
    .event-list {{
      overflow: auto;
      padding: 8px;
    }}
    .event-row {{
      width: 100%;
      height: auto;
      min-height: 78px;
      border: 1px solid transparent;
      background: transparent;
      color: var(--ink);
      border-radius: 8px;
      display: grid;
      grid-template-columns: 78px 1fr;
      gap: 10px;
      align-items: start;
      padding: 10px;
      text-align: left;
      cursor: pointer;
    }}
    .event-row > span:last-child {{
      min-width: 0;
      display: grid;
      gap: 4px;
    }}
    .event-row:hover {{ background: rgba(47, 143, 131, 0.08); }}
    .event-row.active {{
      background: #fffdf7;
      border-color: var(--accent);
    }}
    .event-date {{
      color: var(--accent);
      font-weight: 800;
      font-size: 13px;
      line-height: 1.35;
    }}
    .event-title {{ display: block; font-weight: 800; line-height: 1.35; }}
    .event-summary {{ display: block; color: var(--muted); line-height: 1.5; font-size: 13px; font-weight: 600; }}
    @media (max-width: 1100px) {{
      header {{ grid-template-columns: 1fr; }}
      .source-badge {{ text-align: left; width: fit-content; }}
      main {{ grid-template-columns: 1fr; }}
      .map-column {{ position: static; }}
      .controls {{ grid-template-columns: 1fr; }}
      .button-row {{ grid-template-columns: repeat(2, 1fr); }}
      .quick-index {{ grid-template-columns: 1fr; }}
      svg {{ height: 56vh; min-height: 360px; }}
    }}
    @media (max-width: 560px) {{
      .event-row {{ grid-template-columns: 1fr; }}
      .button-row {{ grid-template-columns: 1fr; }}
      .chapter h2, .detail h2 {{ font-size: 21px; }}
    }}
    /* Reading atlas */
    :root {{
      --paper: #f5f6f4;
      --panel: #ffffff;
      --ink: #202e30;
      --muted: #687777;
      --line: #dde4e1;
      --accent: #b54c39;
      --sea: #dbe8e7;
      --land: #edf0e9;
      --country: #cbd4cb;
      --teal: #28756c;
    }}
    body {{ background: var(--paper); }}
    header {{
      padding: 20px 32px;
      align-items: center;
      border-bottom: 1px solid var(--line);
      background: #fff;
    }}
    .eyebrow {{ color: var(--teal); font-size: 11px; font-weight: 800; margin-bottom: 6px; }}
    h1 {{ font-family: Georgia, "Songti SC", "STSong", serif; font-size: 27px; line-height: 1.3; }}
    .subhead {{ font-size: 13px; margin-top: 3px; }}
    .source-badge {{ border: 0; background: transparent; padding: 0; min-width: 0; color: var(--muted); }}
    main {{
      max-width: 1800px;
      margin: 0 auto;
      padding: 26px 32px 60px;
      grid-template-columns: minmax(0, 1.06fr) minmax(0, .94fr);
      gap: 36px;
    }}
    .map-column {{ display: flex; flex-direction: column; gap: 0; top: 16px; }}
    .controls, .map-wrap, .reader, .timeline {{ border: 0; background: transparent; border-radius: 0; box-shadow: none; }}
    .map-wrap {{ order: 0; padding: 0; gap: 0; }}
    .map-heading {{ display: flex; align-items: end; justify-content: space-between; gap: 16px; padding: 0 0 15px; }}
    .map-kicker {{ color: var(--teal); font-size: 11px; font-weight: 800; margin-bottom: 5px; }}
    .map-heading h2 {{ font-family: Georgia, "Songti SC", "STSong", serif; font-size: 25px; line-height: 1.3; margin: 0; }}
    .map-year {{ color: var(--accent); font-family: Georgia, serif; font-size: 34px; line-height: 1; white-space: nowrap; }}
    svg {{ display: block; width: 100%; height: auto; min-height: 0; aspect-ratio: 1000 / 620; border: 1px solid #cbdad6; border-radius: 3px; background: var(--sea); }}
    .country {{ fill: var(--land); stroke: #d0d9d0; stroke-width: .7; }}
    .historical-country {{ fill: rgba(112, 133, 115, .12); stroke: rgba(94, 112, 101, .58); stroke-width: .9; }}
    .historical-country.precision-low {{ fill: rgba(112, 133, 115, .09); stroke-dasharray: 4 3; }}
    .historical-country.ottoman-core {{ fill: #c56b55; stroke: #884435; stroke-width: 1.5; filter: none; }}
    .historical-country.ottoman-dependent {{ fill: #dfc58e; stroke: #aa8043; stroke-width: 1.2; stroke-dasharray: 5 3; }}
    .region, .region.active {{ fill: none; opacity: 0; stroke: #32766c; stroke-width: 1.7; stroke-dasharray: 4 3; filter: none; pointer-events: none; }}
    .region.active {{ opacity: .85; }}
    .graticule {{ stroke: rgba(98, 132, 126, .13); stroke-width: .6; }}
    .label {{ display: none; font-size: 12px; fill: #283f3b; stroke: #f4f6ef; stroke-width: 4px; font-weight: 700; }}
    .label.active {{ display: block; }}
    .marker.current {{ fill: #233e3a; stroke: #fff; stroke-width: 3; }}
    .legend {{ padding: 13px 0 15px; gap: 8px 15px; font-size: 12px; border-bottom: 1px solid var(--line); }}
    .swatch {{ width: 11px; height: 11px; border-radius: 2px; }}
    .controls {{ order: 1; padding: 17px 0; gap: 12px; grid-template-columns: 1fr 1fr; border-bottom: 1px solid var(--line); }}
    .controls input[type="range"] {{ margin: 0; height: 18px; }}
    .control-field {{ gap: 6px; }}
    .control-label {{ font-size: 11px; font-weight: 700; }}
    select, button {{ height: 36px; border-radius: 4px; background: #fff; border-color: #d4ddda; font-size: 13px; }}
    select {{ width: 100%; }}
    button {{ font-weight: 650; }}
    button:hover {{ border-color: var(--teal); }}
    button:focus-visible, select:focus-visible, input:focus-visible {{ outline: 2px solid #28756c; outline-offset: 2px; }}
    .button-row {{ grid-template-columns: repeat(3, 1fr) minmax(70px, .65fr); }}
    .play {{ background: #254f49; color: #fff; border-color: #254f49; }}
    .timeline {{ order: 2; max-height: 285px; margin-top: 4px; }}
    .timeline-head {{ padding: 15px 0 10px; border: 0; color: var(--ink); font-size: 13px; font-weight: 700; }}
    .timeline-head span:last-child {{ color: var(--muted); font-weight: 400; }}
    .event-list {{ padding: 0; }}
    .event-row {{ min-height: 0; grid-template-columns: 78px minmax(0, 1fr); gap: 10px; border: 0; border-left: 2px solid transparent; border-radius: 0; padding: 10px 12px; }}
    .event-row:hover {{ background: #e9f0ed; }}
    .event-row.active {{ background: #e7efeb; border-color: var(--teal); }}
    .event-date {{ color: var(--accent); font-size: 12px; }}
    .event-title {{ font-size: 14px; }}
    .event-summary {{ display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; font-size: 12px; font-weight: 400; }}
    .reader {{ border-left: 1px solid var(--line); padding-left: 36px; overflow: visible; }}
    .chapter {{ background: transparent; padding: 0 0 22px; }}
    .chapter h2 {{ font-family: Georgia, "Songti SC", "STSong", serif; font-size: 23px; line-height: 1.4; }}
    .chapter p, .detail p {{ color: #40504e; font-size: 15px; line-height: 1.9; }}
    .thesis {{ gap: 0; margin-top: 14px; border-left: 2px solid #8bb5a8; }}
    .thesis div {{ padding: 4px 0 4px 14px; border: 0; background: none; color: #52635f; font-size: 13px; }}
    .detail {{ padding: 26px 0; }}
    .detail h2 {{ font-family: Georgia, "Songti SC", "STSong", serif; font-size: 29px; line-height: 1.35; margin: 0; }}
    .kicker {{ font-size: 12px; margin-bottom: 9px; }}
    .lecture {{ margin-top: 20px; gap: 17px; }}
    .lecture p {{ color: #30423f; font-size: 16px; line-height: 2; }}
    .section {{ border-color: var(--line); margin-top: 24px; padding-top: 20px; }}
    .section h3 {{ color: var(--teal); font-size: 14px; }}
    .takeaways li {{ background: #eaf1ed; border-color: #7ca79a; }}
    .chip {{ background: transparent; border-color: var(--line); }}
    @media (max-width: 1100px) {{
      header {{ grid-template-columns: minmax(0, 1fr) auto; }}
      .source-badge {{ text-align: right; }}
      main {{ grid-template-columns: 1fr; gap: 28px; }}
      .map-column {{ position: static; }}
      .reader {{ border-left: 0; border-top: 1px solid var(--line); padding: 28px 0 0; }}
      .controls {{ grid-template-columns: 1fr 1fr; }}
      .button-row {{ grid-template-columns: repeat(3, 1fr) minmax(70px, .65fr); }}
      svg {{ height: auto; min-height: 0; }}
    }}
    @media (max-width: 560px) {{
      header {{ padding: 16px; grid-template-columns: 1fr; gap: 8px; }}
      h1 {{ font-size: 22px; }}
      .source-badge {{ text-align: left; font-size: 12px; }}
      main {{ padding: 20px 16px 40px; }}
      .map-heading h2 {{ font-size: 20px; }}
      .map-year {{ font-size: 25px; }}
      .controls {{ grid-template-columns: 1fr; }}
      .button-row {{ grid-template-columns: repeat(2, 1fr); }}
      .event-row {{ grid-template-columns: 65px minmax(0, 1fr); }}
      .detail h2 {{ font-size: 25px; }}
    }}
    /* Documentary player */
    :root {{
      --paper: #171c1b;
      --ink: #eef2ec;
      --muted: #a6b4ac;
      --line: #384541;
      --accent: #e8aa78;
      --sea: #354e4c;
      --land: #a9b5a4;
      --teal: #a7c8b0;
    }}
    body {{ background: var(--paper); color: var(--ink); }}
    header {{ background: #171c1b; border-color: var(--line); padding: 15px 28px; }}
    .eyebrow {{ color: #dfaa7b; font-size: 10px; margin-bottom: 3px; }}
    h1 {{ font-size: 22px; color: #f1f1e9; }}
    .subhead {{ color: #a5b4aa; font-size: 12px; }}
    .source-badge {{ color: #a5b4aa; }}
    main {{ max-width: none; margin: 0; padding: 0; gap: 0; grid-template-columns: minmax(0, 1.7fr) minmax(330px, .7fr); align-items: stretch; }}
    .map-column {{ position: sticky; top: 0; align-self: start; padding: 26px 30px 20px; min-width: 0; }}
    .map-heading {{ align-items: center; padding: 0 0 19px; gap: 20px; }}
    .map-heading > div:first-child {{ flex: 1; min-width: 0; }}
    .map-heading h2 {{ color: #f4f2e8; font-size: 25px; }}
    .map-kicker {{ color: #b0c7b4; margin-bottom: 6px; }}
    .map-year {{ font-size: 50px; font-weight: 400; color: #efbd90; }}
    .map-stage {{ position: relative; overflow: hidden; background: var(--sea); }}
    svg {{ border: 0; border-radius: 0; background: var(--sea); }}
    .country {{ fill: #a9b5a4; stroke: #8c9d8f; stroke-width: .65; }}
    .historical-country {{ fill: rgba(234, 225, 200, .15); stroke: rgba(54, 75, 68, .6); stroke-width: 1; }}
    .historical-country.precision-low {{ fill: rgba(234, 225, 200, .12); stroke: rgba(57, 77, 70, .68); }}
    .historical-country.ottoman-core {{ fill: #c47d60; stroke: #694638; stroke-width: 1.7; }}
    .historical-country.ottoman-dependent {{ fill: #d8b978; stroke: #826d43; stroke-width: 1.3; stroke-dasharray: 5 3; }}
    .region, .region.active {{ stroke: #f7e4af; stroke-width: 1.6; stroke-dasharray: 5 4; }}
    .graticule {{ stroke: rgba(231, 237, 222, .12); }}
    .label {{ fill: #fff9e9; stroke: #43574e; stroke-width: 4px; font-size: 14px; }}
    .marker.current {{ fill: #f6d89d; stroke: #253d39; stroke-width: 3; }}
    @media (prefers-reduced-motion: no-preference) {{
      #historicalLayer path {{ animation: map-reveal .45s ease-out both; }}
      @keyframes map-reveal {{ from {{ opacity: .2; }} to {{ opacity: 1; }} }}
    }}
    .legend {{ color: #bdc8be; border-color: var(--line); padding: 11px 0 12px; font-size: 11px; }}
    .map-caption {{ padding: 16px 0 10px; display: grid; grid-template-columns: 58px minmax(0, 1fr); gap: 10px; }}
    .caption-label {{ color: #e4af83; font-size: 11px; font-weight: 700; padding-top: 5px; }}
    .map-caption p {{ margin: 0; color: #e5e9df; font-size: 14px; line-height: 1.7; }}
    .controls {{ border: 0; padding: 12px 0 10px; gap: 10px; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); }}
    .controls input[type="range"] {{ accent-color: #d7a275; }}
    .control-label {{ color: #aebcb2; }}
    select, button {{ background: #242d2a; border-color: #46544e; color: #ebf0e8; border-radius: 3px; }}
    select:focus-visible, button:focus-visible, input:focus-visible {{ outline-color: #e8bd93; }}
    button:hover {{ background: #33423c; border-color: #96b6a4; }}
    .play {{ background: #dfb088; color: #1b2521; border-color: #dfb088; }}
    .play:hover {{ background: #ecc6a4; border-color: #ecc6a4; }}
    .button-row {{ display: grid; flex: 0 0 200px; grid-template-columns: 35px 35px 44px minmax(65px, 1fr); gap: 5px; }}
    .button-row button {{ padding: 0; font-size: 18px; }}
    .button-row select {{ padding: 0 5px; }}
    .timeline {{ max-height: none; margin: 0; padding-top: 8px; border-top: 1px solid var(--line); min-width: 0; }}
    .timeline-head {{ color: #e9eee8; padding: 11px 0; }}
    .event-list {{ display: flex; overflow-x: auto; overflow-y: hidden; gap: 0; padding: 0 0 8px; scrollbar-color: #64766b #26312d; scrollbar-width: thin; }}
    .event-row {{ display: block; flex: 0 0 158px; min-height: 100px; height: 100px; padding: 10px 12px; border: 0; border-top: 2px solid #53645a; background: transparent; color: #d5dfd5; }}
    .event-row > span:last-child {{ display: block; }}
    .event-row:hover {{ background: #28342f; }}
    .event-row.active {{ background: #2e3a33; border-color: #e8ad7d; }}
    .event-date {{ display: block; color: #d7a47b; font-family: Georgia, serif; font-size: 15px; line-height: 1.2; }}
    .event-title {{ margin-top: 7px; font-size: 12px; line-height: 1.4; font-weight: 600; }}
    .event-summary {{ display: none; }}
    .reader {{ background: #222b27; border: 0; border-left: 1px solid var(--line); padding: 28px 28px 48px; min-width: 0; }}
    .detail {{ padding: 0 0 28px; }}
    .detail h2, .chapter h2 {{ color: #f2f1e7; }}
    .detail h2 {{ font-size: 27px; }}
    .kicker {{ color: #e7b287; }}
    .chapter {{ padding: 25px 0 0; border: 0; border-top: 1px solid var(--line); }}
    .chapter h2 {{ font-size: 20px; }}
    .chapter p, .detail p, .lecture p {{ color: #d4ded3; }}
    .lecture p {{ font-size: 15px; line-height: 1.95; }}
    .section {{ border-color: #435149; }}
    .section h3 {{ color: #b6d4bf; }}
    .thesis {{ border-color: #92b69d; }}
    .thesis div {{ color: #b9c8ba; }}
    .takeaways li {{ color: #d4ded3; background: #303e34; border-color: #9dbca4; }}
    .chip {{ color: #b9c8ba; border-color: #526158; }}
    @media (max-width: 1050px) {{
      main {{ grid-template-columns: 1fr; }}
      .map-column {{ position: static; padding: 24px 24px 20px; }}
      .reader {{ border-left: 0; border-top: 1px solid var(--line); padding: 28px 24px 45px; }}
    }}
    @media (max-width: 560px) {{
      header {{ padding: 14px 16px; grid-template-columns: minmax(0, 1fr); }}
      h1 {{ font-size: 19px; }}
      .map-column {{ padding: 21px 16px 18px; }}
      .map-heading h2 {{ font-size: 20px; }}
      .map-year {{ font-size: 34px; }}
      .map-heading {{ flex-wrap: wrap; gap: 12px; }}
      .button-row {{ flex: 0 0 100%; grid-template-columns: 38px 38px 48px 80px; }}
      .map-caption {{ grid-template-columns: 1fr; gap: 4px; }}
      .controls {{ grid-template-columns: 1fr 1fr; }}
      .reader {{ padding: 24px 16px 40px; }}
      .event-row {{ flex-basis: 140px; }}
    }}
    [hidden] {{ display: none !important; }}
    .map-brief {{ border-top: 1px solid var(--line); margin-top: 8px; padding: 16px 0; }}
    .brief-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px 24px; }}
    .brief-grid h3, .map-note h3 {{ color: #e8b58a; font-size: 12px; margin: 0 0 7px; }}
    .brief-grid p, .map-note p {{ color: #d5dfd4; font-size: 13px; line-height: 1.85; margin: 0; }}
    .brief-grid .brief-wide {{ grid-column: 1 / -1; }}
    .map-note {{ border-top: 1px solid var(--line); padding-top: 13px; margin-top: 15px; }}
    .map-note p {{ color: #aebfb2; font-size: 12px; }}
    .place-dot {{ fill: #e0e6d5; stroke: #365149; stroke-width: 1; }}
    .place-label {{ fill: #f8f0da; stroke: #38514a; stroke-width: 3; paint-order: stroke; pointer-events: none; font-size: 14px; }}
    .sea-label {{ fill: #c7dcd6; opacity: .78; font-size: 18px; font-family: Georgia, "Songti SC", serif; text-anchor: middle; pointer-events: none; }}
    .label {{ display: none; opacity: .62; font-size: 15px; }}
    .label.context, .label.active {{ display: block; }}
    .label.active {{ opacity: 1; fill: #fff3c7; }}
    .reader-tabs {{ display: flex; gap: 20px; border-bottom: 1px solid var(--line); margin: 0 0 24px; }}
    .reader-tab {{ flex: 1; height: 40px; border: 0; border-bottom: 2px solid transparent; border-radius: 0; padding: 0 0 10px; background: transparent; color: #aebdb3; }}
    .reader-tab[aria-selected="true"] {{ color: #f5cba5; border-color: #dfb088; }}
    .event-lead {{ border-left: 2px solid #d0a17b; padding-left: 13px; margin-top: 20px !important; }}
    .event-meta {{ color: #aebfb2; font-size: 12px; line-height: 1.8; margin: 14px 0; }}
    .lecture-heading {{ font-size: 13px; color: #b6d4bf; margin: 24px 0 0; }}
    .event-links {{ display: grid; gap: 10px; margin-top: 24px; }}
    .event-link {{ height: auto; min-height: 50px; padding: 10px 12px; text-align: left; line-height: 1.65; font-size: 13px; }}
    .event-link span {{ display: block; color: #b9c8ba; font-size: 11px; }}
    .source-heading {{ margin: 0; font-size: 20px; line-height: 1.6; }}
    .source-meta {{ color: #aebfb2; line-height: 1.8; font-size: 12px; margin: 10px 0 18px; }}
    .source-search {{ display: grid; gap: 8px; margin: 0 0 16px; }}
    .source-search label {{ font-size: 12px; color: #b6d4bf; }}
    .source-search input {{ width: 100%; min-width: 0; height: 38px; background: #1b241f; border: 1px solid #526158; border-radius: 3px; color: #edf1e9; padding: 0 10px; font: inherit; font-size: 14px; }}
    .source-count {{ color: #b7c6bb; font-size: 12px; padding: 0 0 14px; }}
    .source-chunk {{ border-top: 1px solid #3d4c43; padding: 16px 0; }}
    .source-chunk h3 {{ font-family: ui-monospace, monospace; color: #dfb088; font-size: 12px; margin: 0 0 8px; }}
    .source-chunk p {{ color: #d4ded3; line-height: 1.95; font-size: 15px; margin: 0; overflow-wrap: anywhere; }}
    mark {{ background: #d9b582; color: #19231e; padding: 0 2px; }}
    .source-empty {{ color: #cbd7cb; line-height: 1.8; font-size: 14px; }}
    @media (max-width: 560px) {{
      .brief-grid {{ grid-template-columns: 1fr; gap: 16px; }}
      .place-label {{ font-size: 21px; }}
      .sea-label {{ font-size: 23px; }}
      .label {{ font-size: 21px; }}
    }}
  </style>
</head>
<body>
  <header>
    <div>
      <div class="eyebrow">THE MIDDLE EAST · CHAPTER 01</div>
      <h1>中东往事第一章：长文地图阅读版</h1>
      <p class="subhead">从奥斯曼帝国到现代中东</p>
    </div>
    <div class="source-badge" id="sourceBadge"></div>
  </header>

  <main>
    <section class="map-column">
      <section class="controls" aria-label="timeline controls">
        <input id="slider" type="range" min="0" value="0" step="1" aria-label="事件时间线" />
        <div class="control-field"><label class="control-label" for="phaseSelect">历史阶段</label><select id="phaseSelect" aria-label="阶段筛选"></select></div>
        <div class="control-field">
          <label class="control-label" for="layerSelect">当前地图年份</label>
          <select id="layerSelect" aria-label="当前地图年份" title="当前地图年份"></select>
        </div>
      </section>
      <section class="map-wrap">
        <div class="map-heading"><div><div class="map-kicker">历史地图 · 当前事件</div><h2 id="mapTitle"></h2></div><div class="map-year" id="mapYear"></div><div class="button-row">
          <button id="prevBtn" title="上一节点" aria-label="上一节点">‹</button>
          <button id="nextBtn" title="下一节点" aria-label="下一节点">›</button>
          <button class="play" id="playBtn" title="播放" aria-label="播放">▶</button>
          <select id="speedSelect" aria-label="自动播放速度"><option value="5000">5秒</option><option value="8000" selected>8秒</option><option value="12000">12秒</option></select>
        </div></div>
        <div class="map-stage"><svg id="map" viewBox="0 0 1000 620" role="img" aria-label="中东历史地图">
          <rect x="0" y="0" width="1000" height="620" fill="var(--sea)"></rect>
          <g id="graticuleLayer"></g>
          <g id="baseLayer"></g>
          <g id="historicalLayer"></g>
          <g id="regionLayer"></g>
          <g id="labelLayer"></g>
          <g id="geographyLayer"></g>
          <g id="markerLayer"></g>
        </svg></div>
        <div class="legend" id="legend"></div>
        <div class="map-caption"><div class="caption-label">事件概览</div><p id="mapCaption"></p></div>
        <section class="map-brief" id="mapBrief" aria-label="事件详解"></section>
      </section>
      <section class="timeline">
        <div class="timeline-head"><span>时间线</span><span id="countLabel"></span></div>
        <div class="event-list" id="eventList"></div>
      </section>
    </section>

    <section class="reader">
      <div class="reader-tabs" role="tablist" aria-label="阅读内容">
        <button class="reader-tab" id="lectureTab" role="tab" aria-selected="true" aria-controls="lecturePanel" tabindex="0">历史讲义</button>
        <button class="reader-tab" id="transcriptTab" role="tab" aria-selected="false" aria-controls="transcriptPanel" tabindex="-1">播客原文</button>
      </div>
      <div id="lecturePanel" role="tabpanel" aria-labelledby="lectureTab"><article class="detail" id="detail"></article><div class="chapter" id="chapter"></div></div>
      <section id="transcriptPanel" role="tabpanel" aria-labelledby="transcriptTab" hidden>
        <div class="source-search"><label for="transcriptEpisode">播客集数</label><select id="transcriptEpisode" aria-label="播客集数"></select></div>
        <h2 class="source-heading" id="sourceTitle"></h2>
        <p class="source-meta" id="sourceMeta"></p>
        <div class="source-search"><label for="transcriptSearch">搜索本集原文</label><input id="transcriptSearch" type="search" placeholder="人物、地点或条约名称" autocomplete="off" /></div>
        <div class="source-count" id="sourceCount" role="status"></div>
        <div id="sourceChunks"></div>
      </section>
    </section>
  </main>

  <script>
    const DATA = {data};
    const WIDTH = 1000;
    const HEIGHT = 620;
    const BOUNDS = {{ lonMin: -10, lonMax: 58, latMin: 12, latMax: 50 }};
    const events = DATA.events;
    const regions = DATA.regions;
    const regionGeo = DATA.region_geo;
    const historicalLayers = DATA.historical_layers || [];
    const countryFeatures = DATA.boundaries.features;
    const countryByName = new Map(countryFeatures.map(feature => [feature.properties.name, feature]));
    const mapNames = {{ levant: "黎凡特", mesopotamia: "两河流域", arabia: "阿拉伯半岛", armenia: "东安纳托利亚" }};
    const contextRegions = new Set(["balkans", "anatolia", "libya", "egypt", "levant", "mesopotamia", "arabia"]);
    const places = [
      {{ name: "君士坦丁堡", modern: "伊斯坦布尔", point: [28.98, 41.01], regions: ["anatolia", "balkans", "blacksea", "dardanelles"], context: true }},
      {{ name: "安卡拉", point: [32.85, 39.93], regions: ["anatolia"] }},
      {{ name: "雅典", point: [23.73, 37.98], regions: ["greece", "balkans"] }},
      {{ name: "开罗", point: [31.24, 30.04], regions: ["egypt"], context: true }},
      {{ name: "大马士革", point: [36.29, 33.51], regions: ["levant"] }},
      {{ name: "耶路撒冷", point: [35.21, 31.77], regions: ["palestine", "transjordan"] }},
      {{ name: "巴格达", point: [44.36, 33.31], regions: ["mesopotamia"], context: true }},
      {{ name: "麦加", point: [39.86, 21.42], regions: ["hejaz", "arabia"], context: true }},
      {{ name: "利雅得", point: [46.68, 24.71], regions: ["arabia"] }},
    ];
    let visible = events.slice();
    let current = 0;
    let autoplayTimer = null;
    let readerMode = "lecture";
    let transcriptEpisode = events[0].episode;
    let transcriptEventId = events[0].id;

    const slider = document.getElementById("slider");
    const phaseSelect = document.getElementById("phaseSelect");
    const layerSelect = document.getElementById("layerSelect");
    const speedSelect = document.getElementById("speedSelect");
    const playBtn = document.getElementById("playBtn");
    const eventList = document.getElementById("eventList");
    const detail = document.getElementById("detail");
    const chapter = document.getElementById("chapter");
    const markerLayer = document.getElementById("markerLayer");
    const regionLayer = document.getElementById("regionLayer");
    const historicalLayer = document.getElementById("historicalLayer");
    const baseLayer = document.getElementById("baseLayer");
    const labelLayer = document.getElementById("labelLayer");
    const graticuleLayer = document.getElementById("graticuleLayer");
    const countLabel = document.getElementById("countLabel");

    document.getElementById("sourceBadge").textContent = `${{DATA.meta.episode_count}} 集 · ${{events.length}} 个节点 · 长文阅读版`;

    function project(point) {{
      const [lon, lat] = point;
      const x = ((lon - BOUNDS.lonMin) / (BOUNDS.lonMax - BOUNDS.lonMin)) * WIDTH;
      const y = ((BOUNDS.latMax - lat) / (BOUNDS.latMax - BOUNDS.latMin)) * HEIGHT;
      return [x, y];
    }}

    function ringPath(ring) {{
      return ring.map((point, index) => {{
        const [x, y] = project(point);
        return `${{index === 0 ? "M" : "L"}}${{x.toFixed(2)}},${{y.toFixed(2)}}`;
      }}).join(" ") + " Z";
    }}

    function geometryPath(geometry) {{
      if (!geometry) return "";
      if (geometry.type === "Polygon") return geometry.coordinates.map(ringPath).join(" ");
      if (geometry.type === "MultiPolygon") return geometry.coordinates.flatMap(polygon => polygon.map(ringPath)).join(" ");
      return "";
    }}

    function drawGraticule() {{
      const paths = [];
      for (let lon = -10; lon <= 60; lon += 10) {{
        const [x1, y1] = project([lon, BOUNDS.latMin]);
        const [x2, y2] = project([lon, BOUNDS.latMax]);
        paths.push(`<path class="graticule" d="M${{x1.toFixed(1)}},${{y1.toFixed(1)}} L${{x2.toFixed(1)}},${{y2.toFixed(1)}}"></path>`);
      }}
      for (let lat = 15; lat <= 50; lat += 5) {{
        const [x1, y1] = project([BOUNDS.lonMin, lat]);
        const [x2, y2] = project([BOUNDS.lonMax, lat]);
        paths.push(`<path class="graticule" d="M${{x1.toFixed(1)}},${{y1.toFixed(1)}} L${{x2.toFixed(1)}},${{y2.toFixed(1)}}"></path>`);
      }}
      graticuleLayer.innerHTML = paths.join("");
    }}

    function drawBaseMap() {{
      baseLayer.innerHTML = countryFeatures.map(feature => {{
        const d = geometryPath(feature.geometry);
        return `<path class="country" d="${{d}}"><title>${{feature.properties.name}}</title></path>`;
      }}).join("");
    }}

    function historicalLayerById(id) {{
      return historicalLayers.find(layer => layer.id === id);
    }}

    function suggestedLayer(event) {{
      const year = Math.floor(Number(event.year));
      if (year < 1500) return "y1500";
      if (year >= 1500 && year < 1700) return "y1600";
      if (year >= 1878 && year < 1912) return "y1878";
      if (year >= 1912 && year < 1920) return "y1913";
      if (year >= 1920 && year < 1923) return "y1920";
      if (year >= 1923) return "y1923";
      return "";
    }}

    function ottomanClass(properties) {{
      const name = String(properties.name || "").toLowerCase();
      const subject = String(properties.subject || "").toLowerCase();
      const partOf = String(properties.part_of || "").toLowerCase();
      const isCore = name === "ottoman empire" || name === "ottoman sultanate";
      const isAttached = subject.includes("ottoman") || partOf.includes("ottoman");
      if (isCore) return "ottoman-core";
      if (isAttached) return "ottoman-dependent";
      return "";
    }}

    function ottomanRank(feature) {{
      const cls = ottomanClass(feature.properties || {{}});
      if (cls === "ottoman-core") return 2;
      if (cls === "ottoman-dependent") return 1;
      return 0;
    }}

    function layerHasOttomanRole(layer, role) {{
      return Boolean(layer && layer.features.some(feature => ottomanClass(feature.properties || {{}}) === role));
    }}

    function renderHistoricalPaths(layerId, extraClass = "") {{
      const layer = historicalLayerById(layerId);
      if (!layer) return "";
      return layer.features.slice().sort((a, b) => ottomanRank(a) - ottomanRank(b)).map(feature => {{
        const d = geometryPath(feature.geometry);
        const precision = Number(feature.properties.precision || 3);
        const ottoman = ottomanClass(feature.properties || {{}});
        const cls = ["historical-country", extraClass, precision < 3 ? "precision-low" : "", ottoman].filter(Boolean).join(" ");
        const name = feature.properties.name || feature.properties.subject || "Historical boundary";
        const role = ottoman === "ottoman-core" ? "奥斯曼本体" : ottoman === "ottoman-dependent" ? "奥斯曼附庸/势力范围" : "";
        return `<path class="${{cls}}" d="${{d}}"><title>${{name}}${{role ? ` · ${{role}}` : ""}}</title></path>`;
      }}).join("");
    }}

    function drawHistoricalLayer(layerId) {{
      historicalLayer.innerHTML = renderHistoricalPaths(layerId);
    }}

    function polygonPath(points) {{
      return ringPath(points);
    }}

    function regionD(regionId) {{
      const geo = regionGeo[regionId] || {{}};
      const parts = [];
      (geo.countries || []).forEach(name => {{
        const feature = countryByName.get(name);
        if (feature) parts.push(geometryPath(feature.geometry));
      }});
      if (geo.polygon) parts.push(polygonPath(geo.polygon));
      return parts.join(" ");
    }}

    function drawRegions() {{
      regionLayer.innerHTML = Object.entries(regions).map(([id, region]) => {{
        const d = regionD(id);
        if (!d) return "";
        return `<path id="region-${{id}}" class="region" d="${{d}}" fill="${{region.color}}"><title>${{region.label}}</title></path>`;
      }}).join("");
    }}

    function drawLabels() {{
      labelLayer.innerHTML = Object.entries(regionGeo).map(([id, geo]) => {{
        if (!geo.label_lonlat || !regions[id]) return "";
        const [x, y] = project(geo.label_lonlat);
        return `<text id="label-${{id}}" class="label ${{contextRegions.has(id) ? "context" : ""}}" x="${{x.toFixed(1)}}" y="${{y.toFixed(1)}}">${{mapNames[id] || regions[id].label}}</text>`;
      }}).join("");
    }}

    function escapeHTML(value) {{
      return String(value).replace(/[&<>"']/g, char => ({{ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }})[char]);
    }}

    function drawGeography(event) {{
      const compact = window.matchMedia("(max-width: 560px)").matches;
      const fontSize = compact ? 21 : 14;
      const blocked = Array.from(labelLayer.querySelectorAll(".context, .active")).map(label => {{
        const box = label.getBBox();
        return {{ x: box.x - 4, y: box.y - 4, width: box.width + 8, height: box.height + 8 }};
      }});
      const seaNames = [
        {{ name: "地中海", point: [16, 35] }},
        {{ name: "黑海", point: [34, 44] }},
        {{ name: "红海", point: [36.5, 21.2], angle: -55 }},
        {{ name: "波斯湾", point: [51.5, 27.1], angle: -28 }},
        {{ name: "里海", point: [51.5, 41.8] }},
      ];
      const markup = seaNames.map(place => {{
        const [x, y] = project(place.point);
        return `<text class="sea-label" x="${{x}}" y="${{y}}" transform="rotate(${{place.angle || 0}} ${{x}} ${{y}})">${{place.name}}</text>`;
      }});
      const candidates = places.filter(place => place.context || place.regions.some(region => event.regions.includes(region)));
      candidates.forEach(place => {{
        const [x, y] = project(place.point);
        const name = place.modern && Number(event.year) >= 1930 ? place.modern : place.name;
        const width = name.length * fontSize;
        const offsets = [[8, -8], [8, 20], [-width - 8, -8], [-width - 8, 20], [12, -27]];
        const position = offsets.find(([dx, dy]) => {{
          const box = {{ x: x + dx, y: y + dy - fontSize, width, height: fontSize + 4 }};
          return box.x >= 4 && box.x + box.width <= WIDTH - 4 && box.y >= 4 && box.y + box.height <= HEIGHT - 4 && !blocked.some(other => box.x < other.x + other.width && box.x + box.width > other.x && box.y < other.y + other.height && box.y + box.height > other.y);
        }});
        if (!position) return;
        const [dx, dy] = position;
        blocked.push({{ x: x + dx - 4, y: y + dy - fontSize - 3, width: width + 8, height: fontSize + 9 }});
        markup.push(`<circle class="place-dot" cx="${{x}}" cy="${{y}}" r="3"></circle><text class="place-label" x="${{x + dx}}" y="${{y + dy}}">${{name}}</text>`);
      }});
      document.getElementById("geographyLayer").innerHTML = markup.join("");
    }}

    function renderMapBrief(event) {{
      const reading = event.reading;
      const layer = historicalLayerById(layerSelect.value);
      document.getElementById("mapBrief").innerHTML = `
        <div class="brief-grid">
          <div><h3>发生了什么</h3><p>${{reading.happened}}</p></div>
          <div><h3>为什么重要</h3><p>${{reading.importance}}</p></div>
          <div class="brief-wide"><h3>版图与控制权</h3><p>${{event.territory_change}}</p></div>
          <div class="brief-wide"><h3>地图怎么读</h3><p>${{reading.map}}</p></div>
          <div><h3>主要参与者</h3><p>${{event.actors.join("、")}}</p></div>
          <div><h3>相关地区</h3><p>${{event.regions_label}}</p></div>
        </div>
        <div class="map-note"><h3>当前画面依据</h3><p>${{layer ? `${{event.date}} 年的事件 · 当前边界数据为 ${{layer.source_year}} 年。${{layer.note}}` : "当前显示现代边界底图，用于定位事件涉及的地理区域。"}} 虚线关注区域为讲解示意，不代表事件当年的国界。</p></div>
      `;
    }}

    function renderTranscript(event) {{
      const transcript = (DATA.episode_transcripts || {{}})[transcriptEpisode || event.episode];
      document.getElementById("transcriptEpisode").value = transcriptEpisode;
      const query = document.getElementById("transcriptSearch").value.trim();
      const title = document.getElementById("sourceTitle");
      const sourceMeta = document.getElementById("sourceMeta");
      const sourceCount = document.getElementById("sourceCount");
      const sourceChunks = document.getElementById("sourceChunks");
      title.textContent = transcript ? transcript.title : `第 ${{event.episode}} 集`;
      sourceMeta.textContent = "语音识别转写，保留原有表述，专有名词可能有识别误差。下方时间标记对应本集音频。";
      if (!transcript) {{
        sourceCount.textContent = "";
        sourceChunks.innerHTML = '<p class="source-empty">本集转写尚未载入。</p>';
        return;
      }}
      const matched = transcript.chunks.filter(chunk => !query || chunk.text.toLocaleLowerCase().includes(query.toLocaleLowerCase()));
      sourceCount.textContent = query ? `找到 ${{matched.length}} 个相关段落 / 全集 ${{transcript.chunks.length}} 段` : `本集全文 · ${{transcript.characters.toLocaleString("zh-CN")}} 字 · ${{transcript.chunks.length}} 段`;
      const highlight = text => {{
        if (!query) return escapeHTML(text);
        let result = "";
        let offset = 0;
        const lower = text.toLocaleLowerCase();
        const needle = query.toLocaleLowerCase();
        let index = lower.indexOf(needle);
        while (index >= 0) {{
          result += escapeHTML(text.slice(offset, index)) + `<mark>${{escapeHTML(text.slice(index, index + query.length))}}</mark>`;
          offset = index + query.length;
          index = lower.indexOf(needle, offset);
        }}
        return result + escapeHTML(text.slice(offset));
      }};
      sourceChunks.innerHTML = matched.length ? matched.map(chunk => `<section class="source-chunk"><h3>${{chunk.time}}</h3><p>${{highlight(chunk.text)}}</p></section>`).join("") : '<p class="source-empty">没有找到匹配的段落。可以缩短关键词，或尝试人物、地点的其他译名。</p>';
    }}

    function setReaderMode(mode) {{
      readerMode = mode;
      const lecture = mode === "lecture";
      document.getElementById("lecturePanel").hidden = !lecture;
      document.getElementById("transcriptPanel").hidden = lecture;
      [["lectureTab", lecture], ["transcriptTab", !lecture]].forEach(([id, selected]) => {{
        const tab = document.getElementById(id);
        tab.setAttribute("aria-selected", String(selected));
        tab.tabIndex = selected ? 0 : -1;
      }});
      if (!lecture) renderTranscript(visible[current]);
    }}

    function unique(values) {{
      return Array.from(new Set(values));
    }}

    function setupControls() {{
      phaseSelect.innerHTML = ["全部阶段", ...unique(events.map(e => e.phase))].map(p => `<option value="${{p}}">${{p}}</option>`).join("");
      layerSelect.innerHTML = [`<option value="">现代边界底图</option>`, ...historicalLayers.map(layer => `<option value="${{layer.id}}">${{layer.label}}（用${{layer.source_year}}）</option>`)].join("");
      phaseSelect.addEventListener("change", () => {{
        const phase = phaseSelect.value;
        visible = phase === "全部阶段" ? events.slice() : events.filter(e => e.phase === phase);
        setCurrent(0);
      }});
      layerSelect.addEventListener("change", () => {{
        drawHistoricalLayer(layerSelect.value);
        render();
      }});
    }}

    function stopAutoplay() {{
      if (autoplayTimer) clearInterval(autoplayTimer);
      autoplayTimer = null;
      playBtn.textContent = "▶";
      playBtn.title = "播放";
      playBtn.setAttribute("aria-label", "播放");
    }}

    function startAutoplay() {{
      stopAutoplay();
      if (current >= visible.length - 1) setCurrent(0);
      playBtn.textContent = "⏸";
      playBtn.title = "暂停";
      playBtn.setAttribute("aria-label", "暂停");
      autoplayTimer = setInterval(() => {{
        if (current >= visible.length - 1) {{
          stopAutoplay();
          return;
        }}
        setCurrent(current + 1, true);
      }}, Number(speedSelect.value));
    }}

    function setCurrent(index, autoLayer = true) {{
      current = Math.max(0, Math.min(index, visible.length - 1));
      if (autoLayer) {{
        layerSelect.value = suggestedLayer(visible[current]);
        drawHistoricalLayer(layerSelect.value);
      }}
      render();
    }}

    function clearActiveRegions() {{
      document.querySelectorAll(".region").forEach(el => el.classList.remove("active"));
    }}

    function renderChapter() {{
      chapter.innerHTML = `
        <h2>${{DATA.chapter_reading.title}}</h2>
        <p>${{DATA.chapter_reading.lead}}</p>
        <div class="thesis">
          ${{DATA.chapter_reading.thesis.map(item => `<div>${{item}}</div>`).join("")}}
        </div>
      `;
    }}

    function renderMap(event) {{
      clearActiveRegions();
      document.querySelectorAll(".label").forEach(el => el.classList.remove("active"));
      document.getElementById("mapTitle").textContent = event.title;
      document.getElementById("mapYear").textContent = event.date;
      document.getElementById("mapCaption").textContent = event.reading.overview;
      event.regions.forEach(id => {{
        const el = document.getElementById(`region-${{id}}`);
        if (el) el.classList.add("active");
        const label = document.getElementById(`label-${{id}}`);
        if (label) label.classList.add("active");
      }});
      drawGeography(event);
      markerLayer.innerHTML = "";
      [event].forEach(item => {{
        const [x, y] = project(item.marker_lonlat);
        const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
        circle.setAttribute("cx", x.toFixed(2));
        circle.setAttribute("cy", y.toFixed(2));
        circle.setAttribute("r", item.id === event.id ? 8.5 : 5);
        circle.setAttribute("class", item.id === event.id ? "marker current" : item.year <= event.year ? "marker past" : "marker");
        circle.addEventListener("click", () => {{
          const nextIndex = visible.findIndex(e => e.id === item.id);
          if (nextIndex >= 0) setCurrent(nextIndex);
        }});
        markerLayer.appendChild(circle);
      }});
    }}

    function renderLegend(event) {{
      const layer = historicalLayerById(layerSelect.value);
      const layerText = layer ? `<span><i class="swatch" style="background:#a9b5a4"></i>历史边界 · 数据年份 ${{layer.source_year}}</span>` : `<span><i class="swatch" style="background:#a9b5a4"></i>现代边界底图</span>`;
      const showOttomanCore = layerHasOttomanRole(layer, "ottoman-core");
      const showOttomanDependent = layerHasOttomanRole(layer, "ottoman-dependent");
      const ottomanText = [
        showOttomanCore ? `<span><i class="swatch" style="background:#c47d60;border-color:#694638"></i>奥斯曼本体</span>` : "",
        showOttomanDependent ? `<span><i class="swatch" style="background:#d8b978;border:2px dashed #826d43"></i>附庸/势力范围</span>` : "",
      ].join("");
      document.getElementById("legend").innerHTML = layerText + ottomanText + `<span><i class="swatch" style="background:transparent;border:2px dashed #f7e4af"></i>事件关注区域（示意）</span><span><i class="swatch" style="background:#f6d89d;border-radius:50%"></i>事件地点</span>`;
    }}

    function renderDetail(event) {{
      const reading = event.reading;
      const layer = historicalLayerById(layerSelect.value);
      const showOttomanCore = layerHasOttomanRole(layer, "ottoman-core");
      const showOttomanDependent = layerHasOttomanRole(layer, "ottoman-dependent");
      const ottomanNote = [
        showOttomanCore ? "红褐色表示奥斯曼帝国本体。" : "",
        showOttomanDependent ? "琥珀色虚线表示数据中 subject 或 part_of 指向奥斯曼的附庸、属国或势力范围。" : "",
      ].join("");
      const layerNote = layer ? `<div class="section"><h3>当前历史地图</h3><p>${{layer.label}}：实际使用 ${{layer.source_year}} 年数据。${{layer.note}}${{ottomanNote}}</p></div>` : "";
      const actors = event.actors.map(actor => `<span class="chip">${{actor}}</span>`).join("");
      const sectionTitles = ["历史位置", "局势背景", "事件经过", "版图与控制权", "影响与后续"];
      const lecture = (reading.lecture || reading.overview).split(/\\n\\n+/).map((paragraph, index) => `<section><h3 class="lecture-heading">${{String(index + 1).padStart(2, "0")}} · ${{sectionTitles[index] || "补充说明"}}</h3><p>${{paragraph}}</p></section>`).join("");
      const eventIndex = events.findIndex(item => item.id === event.id);
      const adjacent = [events[eventIndex - 1], events[eventIndex + 1]].map((item, index) => item ? `<button class="event-link" data-event-id="${{item.id}}"><span>${{index === 0 ? "时间线前一节点" : "时间线后一节点"}} · ${{item.date}}</span>${{item.title}}</button>` : "").join("");
      detail.innerHTML = `
        <div class="kicker">${{event.date}} · ${{event.phase}} · ${{event.episode}} ${{event.audio_start}}</div>
        <h2>${{event.title}}</h2>
        <p class="event-lead">${{reading.overview}}</p>
        <div class="event-meta">主要参与者：${{event.actors.join("、")}}<br>涉及地区：${{event.regions_label}}</div>
        <div class="lecture">${{lecture}}</div>
        <div class="section quick-index">
          <div><h3>背景</h3><p>${{reading.background}}</p></div>
          <div><h3>地图怎么读</h3><p>${{reading.map}}</p></div>
          <div><h3>发生了什么</h3><p>${{reading.happened}}</p></div>
          <div><h3>为什么重要</h3><p>${{reading.importance}}</p></div>
        </div>
        <div class="section"><h3>记住这几点</h3><ul class="takeaways">${{reading.takeaways.map(item => `<li>${{item}}</li>`).join("")}}</ul></div>
        ${{layerNote}}
        <div class="meta"><span class="chip">${{event.regions_label}}</span>${{actors}}</div>
        <nav class="event-links" aria-label="相邻时间节点">${{adjacent}}</nav>
      `;
      detail.querySelectorAll(".event-link").forEach(button => button.addEventListener("click", () => {{
        let index = visible.findIndex(item => item.id === button.dataset.eventId);
        if (index < 0) {{
          visible = events.slice();
          phaseSelect.value = "全部阶段";
          index = visible.findIndex(item => item.id === button.dataset.eventId);
        }}
        setCurrent(index);
      }}));
    }}

    function renderList() {{
      eventList.innerHTML = visible.map((event, index) => `
        <button class="event-row ${{index === current ? "active" : ""}}" data-index="${{index}}">
          <span class="event-date">${{event.date}}</span>
          <span>
            <span class="event-title">${{event.title}}</span>
            <span class="event-summary">${{event.reading.overview}}</span>
          </span>
        </button>
      `).join("");
      eventList.querySelectorAll(".event-row").forEach(row => {{
        row.addEventListener("click", () => setCurrent(Number(row.dataset.index)));
      }});
      const active = eventList.querySelector(".event-row.active");
      if (active) {{
        const left = active.offsetLeft - eventList.offsetLeft;
        if (left < eventList.scrollLeft || left + active.offsetWidth > eventList.scrollLeft + eventList.clientWidth) {{
          eventList.scrollLeft = left - eventList.clientWidth / 2 + active.offsetWidth / 2;
        }}
      }}
      countLabel.textContent = `${{current + 1}} / ${{visible.length}}`;
    }}

    function render() {{
      if (!visible.length) return;
      slider.max = Math.max(visible.length - 1, 0);
      slider.value = current;
      const event = visible[current];
      if (event.id !== transcriptEventId) {{
        transcriptEpisode = event.episode;
        transcriptEventId = event.id;
      }}
      renderMap(event);
      renderLegend(event);
      renderMapBrief(event);
      renderDetail(event);
      renderList();
      if (readerMode === "transcript") renderTranscript(event);
    }}

    document.getElementById("lectureTab").addEventListener("click", () => setReaderMode("lecture"));
    document.getElementById("transcriptTab").addEventListener("click", () => setReaderMode("transcript"));
    document.getElementById("transcriptEpisode").innerHTML = Object.entries(DATA.episode_transcripts || {{}}).sort(([a], [b]) => Number(a.split(".")[1] || 999) - Number(b.split(".")[1] || 999)).map(([id, episode]) => `<option value="${{escapeHTML(id)}}">${{escapeHTML(episode.title)}}</option>`).join("");
    document.getElementById("transcriptEpisode").addEventListener("change", event => {{
      transcriptEpisode = event.target.value;
      renderTranscript(visible[current]);
    }});
    document.getElementById("transcriptSearch").addEventListener("input", () => renderTranscript(visible[current]));
    document.querySelector(".reader-tabs").addEventListener("keydown", event => {{
      if (event.key !== "ArrowLeft" && event.key !== "ArrowRight") return;
      event.preventDefault();
      event.stopPropagation();
      const mode = readerMode === "lecture" ? "transcript" : "lecture";
      setReaderMode(mode);
      document.getElementById(mode === "lecture" ? "lectureTab" : "transcriptTab").focus();
    }});
    window.addEventListener("resize", () => drawGeography(visible[current]));
    slider.addEventListener("input", () => setCurrent(Number(slider.value)));
    playBtn.addEventListener("click", () => autoplayTimer ? stopAutoplay() : startAutoplay());
    speedSelect.addEventListener("change", () => {{ if (autoplayTimer) startAutoplay(); }});
    document.getElementById("prevBtn").addEventListener("click", () => setCurrent(current - 1));
    document.getElementById("nextBtn").addEventListener("click", () => setCurrent(current + 1));
    window.addEventListener("keydown", event => {{
      if (["INPUT", "SELECT", "TEXTAREA"].includes(event.target.tagName)) return;
      if (event.key === "ArrowLeft") setCurrent(current - 1);
      if (event.key === "ArrowRight") setCurrent(current + 1);
    }});

    drawGraticule();
    drawBaseMap();
    drawRegions();
    drawLabels();
    setupControls();
    renderChapter();
    setCurrent(0);
  </script>
</body>
</html>
"""


def main() -> None:
    payload = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    payload = enrich(payload)
    DATA_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    READING_MD_PATH.write_text(build_reading_markdown(payload), encoding="utf-8")
    HTML_PATH.write_text(build_html(payload), encoding="utf-8")
    print(f"wrote {DATA_PATH}")
    print(f"wrote {READING_MD_PATH}")
    print(f"wrote {HTML_PATH}")


if __name__ == "__main__":
    main()
