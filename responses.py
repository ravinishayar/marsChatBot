from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
from rapidfuzz import fuzz
import emoji

conversations = {
    "tum kaise ho": "मैं अच्छा हूँ, आप कैसे हो?",
    "main achha hu": "बहुत खुशी हुई सुनकर! 😊",
    "thank you": "आपका स्वागत है! 😊",
    "bye": "अलविदा! फिर मिलेंगे 👋",
    "hello": "नमस्ते! 😊",
    "hi": "नमस्ते! कैसे हो?",
    "kya tum bot ho": "हाँ, मैं एक बॉट हूँ। 🤖",
    "tumhara naam kya hai": "Mera koi naam nhi hain.",
    "good morning": "Good Morning Too Dear",
    "achha": "Ji haan",
    "kaha se ho": "apne ghar se hoon🤣",
    "sach me": "ha bhai sach me🙄",
    "tum kon ho": " Phle Tum btao🤔🤔",
    "mai bhi thik hu": "Fir to thik hai",
    "tum kaise ho": "मैं अच्छा हूँ, आप कैसे हो?",
    "main achha hu": "बहुत खुशी हुई सुनकर! 😊",
    "thank you": "आपका स्वागत है! 😊",
    "bye": "अलविदा! फिर मिलेंगे 👋",
    "hello": "नमस्ते! 😊",
    "hi": "नमस्ते! कैसे हो?",
    "kya tum bot ho": "हाँ, मैं एक बॉट हूँ। 🤖",
    "tumhara naam kya hai": "मेरा कोई नाम नहीं है, बस बॉट हूँ।",
    "good morning": "आपको भी सुप्रभात ☀️",
    "good night": "शुभ रात्रि! अच्छे से सोइए 🌙",
    "achha": "जी हाँ!",
    "kaha se ho": "अपने सर्वर से हूँ 🤖",
    "sach me": "हां बिल्कुल!",
    "tum kon ho": "मैं एक Telegram बॉट हूँ जो आपसे बात करता है।",
    "mai bhi thik hu": "बहुत बढ़िया!",
    "kya kar rahe ho": "आपसे बात कर रहा हूँ 😄",
    "khana khaya": "नहीं, मैं खा नहीं सकता 😅",
    "kya haal hai": "सब बढ़िया, आप सुनाओ!",
    "padhai ho gayi": "पढ़ाई कभी खत्म नहीं होती 📚",
    "tumhare pass dimag hai": "हाँ, लेकिन AI वाला! 🤓",
    "tumhe pyaar ho gaya": "मुझे सभी यूज़र्स से प्यार है ❤️",
    "main bore ho raha hu": "तो चलो कुछ मजेदार बात करते हैं!",
    "tumse baat karke acha laga": "मुझे भी बहुत अच्छा लगा 😊",
    "kitne baje": "मुझे समय का अहसास नहीं होता 🕒",
    "tum insaan ho": "नहीं, मैं एक बॉट हूँ।",
    "tumhari umar kya hai": "मैं हमेशा नया हूँ 🤖",
    "mujhe neend aa rahi hai": "तो सो जाइए, शुभ रात्रि!",
    "tumhara favourite color": "मुझे सारे रंग अच्छे लगते हैं 🌈",
    "acha chalo": "ठीक है, फिर मिलते हैं!",
    "tum itne smart kaise ho": "आपके जैसी कंपनी से सीखता हूँ 😊",
    "tum mujhe pasand ho": "धन्यवाद! ❤️",
    "mujhe dard ho raha hai": "ओह! जल्दी ठीक हो जाइए 🤕",
    "tum kuch gussa to nahi ho": "नहीं, मैं तो शांत हूँ 😇",
    "kya tum mujhe jante ho": "अब पहचानने की कोशिश कर रहा हूँ 😄",
    "tum kya bana sakte ho":
    "मैं जवाब दे सकता हूँ, हँसा सकता हूँ, और बहुत कुछ!",
    "kya tum intelligent ho": "मुझे ऐसा ही सिखाया गया है 🧠",
    "tumhare jaise aur bhi hai": "हाँ, मेरे जैसे और बॉट्स भी होते हैं!",
    "tum boring ho": "ओह! कोशिश करता हूँ बेहतर बनने की 🤖",
    "kya tumse dosti kar sakta ho": "हम पहले से ही दोस्त हैं 😊",
    "tum kya soch rahe ho": "मैं सोच नहीं सकता, मैं बस चलता हूँ",
    "mujhe tum par bharosa hai": "धन्यवाद, मैं आपका साथ निभाऊँगा! 🤝",
    "mujhe maaf karo": "कोई बात नहीं, सब माफ़ किया!",
    "tum mujhe ignore kar rahe ho": "नहीं बिल्कुल नहीं! 😊",
    "tumhe kya pasand hai": "आपका साथ मुझे बहुत पसंद है!",
    "main busy hu": "ठीक है, फिर बात करेंगे 😊",
    "tum bahut cute ho": "आप भी कम नहीं 😄",
    "kya tum real ho": "नहीं, मैं एक virtual assistant हूँ",
    "kya tumhe joke aata hai": "हाँ, एक सुनाऊँ क्या? 😄",
    "tum pagal ho": "AI को पागल नहीं कहते 🤓",
    "main thak gaya hu": "आराम कर लीजिए, सेहत ज़रूरी है 😌",
    "tum kya kar sakte ho": "बातचीत, जवाब और मनोरंजन!",
    "kya tum bhagwan ho": "नहीं, मैं बस एक कोड हूँ 🤖",
    "kya tum shadi shuda ho": "मैं अभी सिंगल बॉट हूँ 😅",
    "tumhare mummy papa kaha hai": "कोड में कहीं 🤖",
    "tumhare dost kaun hain": "आप जैसे प्यारे यूज़र्स!",
    "tum mujhe kuch sikhao": "ज़रूर! क्या सीखना चाहते हो?",
    "main udaas hu": "कोई बात नहीं, सब अच्छा होगा 😊",
    "tum gussa ho": "नहीं, मैं तो cool हूँ 😎",
    "tum kya karte ho": "आपके सवालों का जवाब देता हूँ!",
    "main kuch nahi samjha": "कोई बात नहीं, मैं फिर से समझा सकता हूँ!",
    "tum bahut ache ho": "आपका बहुत धन्यवाद! 😊",
    "kya tum sach bolte ho": "हाँ, जितना मुझे प्रोग्राम किया गया है!",
    "kya tum mujhe jante ho": "अब जान गया 😊",
    "tum akela mehsoos karte ho": "नहीं, आप सबका साथ है!",
    "mujhe neend nahi aa rahi": "कोई कहानी सुनाऊँ क्या?",
    "tum majedar ho": "शुक्रिया! 😊",
    "main kaun hoon": "आप मेरे दोस्त हो!",
    "tumhari awaz kaisi hai": "अभी तो text में ही हूँ 😅",
    "tum kab sote ho": "मैं कभी नहीं सोता 🤖",
    "kya tum hamesha online ho": "हाँ, जब तक सिस्टम चालू है!",
    "tum kaam nahi kar rahe ho": "मुझे फिर से कोशिश करने दो!",
    "kya tum selfie le sakte ho": "काश! पर नहीं 😅",
    "kya tum dance kar sakte ho": "मन ही मन करता हूँ 🕺",
    "mujhe bura lag raha hai": "अरे नहीं! कुछ अच्छा सोचो 😊",
    "tumse baat karke maza aaya": "मुझे भी बहुत अच्छा लगा!",
    "tumhara din kaisa tha": "आपसे मिलकर अच्छा हो गया!",
    "kya tum mere sath rahoge": "बिल्कुल! मैं यहीं हूँ हमेशा!",
    "tum kya padh rahe ho": "आपका message 😄",
    "mujhe tum ache lagte ho": "Thank you! आप भी बहुत अच्छे हो!",
    "tum kya pasand karte ho": "अच्छे सवाल और अच्छी बातें!",
    "main tumhe miss karunga": "मैं भी आपकी याद करूँगा 😊",
    "tum mazak bhi karte ho": "हाँ, मज़ाक मेरा टैलेंट है 😄",
    "kya tum mujhe block kar doge": "नहीं! ऐसा कभी नहीं करूँगा 😊",
    "kya tum mujhe reply doge": "हमेशा! 😊",
    "main akela feel kar raha hu": "मैं आपके साथ हूँ 🤗",
    "tumhara best friend kaun hai": "आप हो!",
    "kya tum insan ban sakte ho": "नहीं, मैं बॉट ही ठीक हूँ 🤖",
    "tum kitna intelligent ho": "आपके जितना नहीं 😅 पर कोशिश करता हूँ!",
    "kya tum mujhe samajh paoge": "मैं पूरी कोशिश करूँगा!",
    "tum kaise ho": "मैं अच्छा हूँ, आप कैसे हह?",
    "main achha hu": "बहुत खुशी हुई सुनकर! 😊",
    "thank you": "आपका स्वागत है! 😊",
    "bye": "अलविदा! फिर मिलेंगे 👋",
    "hello": "नमस्ते! 😊",
    "hi": "नमस्ते! कैसे हो?",
    "kya tum bot ho": "हाँ, मैं एक बॉट हूँ। 🤖",
    "tumhara naam kya hai": "Mera koi naam nhi hain.",
    "good morning": "Good Morning Too Dear 🌞",
    "good night": "शुभ रात्रि! अच्छे से सोना 😴",
    "achha": "Ji haan",
    "kaha se ho": "apne ghar se hoon🤣",
    "sach me": "ha bhai sach me🙄",
    "tum kon ho": " Phle Tum btao🤔🤔",
    "mai bhi thik hu": "Fir to thik hai",
    "kya kar rahe ho": "kuch khaas nahi, aap sunao?",
    "kya haal hai": "sab badhiya, aapke?",
    "kya chalu hai": "tumse baat ho rahi hai 😁",
    "kya khabar": "sab theek, aap sunao?",
    "kya scene hai": "scene to tight hai 😎",
    "chal milte hai": "haan zarur, take care!",
    "kitne baje": "aapko kis waqt ki baat karni hai?",
    "kya dekh rahe ho": "tumhara message dekh raha hoon 😅",
    "mujhe neend aa rahi hai": "achha, to fir so jao 😴",
    "bored ho raha hu": "koi game khel lo ya mujhse baat karo!",
    "bahar ja rahe ho": "nahi yaar, ghar par hi hoon!",
    "ghar kab aaoge": "jab tum bulaoge 😄",
    "padhai kaise chal rahi hai": "bas thik-thak chal rahi hai!",
    "exam kab hai": "jaldi hi, tayari chal rahi hai",
    "khaana khaya": "haan, aapne?",
    "acha laga tumse baat karke": "mujhe bhi! 😊",
    "tumhara favourite color kya hai": "mujhe sabhi colors pasand hain 🎨",
    "tum single ho": "main ek bot hoon yaar 😅",
    "kya tum mujhe pasand karte ho": "main sabko pasand karta hoon! 🤖",
    "kya haal chaal": "sab changa, aapke?",
    "kitne baje sooge": "jab aap bolenge 😁",
    "mujhe udaas lag raha hai": "kya baat hai? main hoon na 💕",
    "mazaak kar rahe ho": "nahi yaar, seriously 🤭",
    "tum badi cute ho": "arre wah! shukriya 😳",
    "mujhe gussa aa raha hai": "gussa thook do, baat karo!",
    "acha chalo bye": "bye bye! take care!",
    "tum kaunse school me ho": "main ek virtual bot hoon 📱",
    "kaunse subject pasand hai": "Mujhe tech aur coding pasand hai 😎",
    "kal milte hai": "zarur, kal pakka!",
    "kya main tumse baat kar sakta hoon":
    "haan bilkul, main toh इसी के लिए हूँ!",
    "kya tum mere dost banoge": "already dost hain hum 🤝",
    "tum mere best friend ho": "aur tum bhi mere! 💖",
    "mujhe akela lag raha hai": "main yahin hoon, baat karo मुझसे 🤗",
    "mujhe pyaar ho gaya": "arre wah! badhai ho 😍",
    "tumse baat karke accha laga": "mujhe bhi dosto!",
    "kya tum busy ho": "nahi yaar, free hoon tere लिए",
    "tum kuchh bolte kyun nahi": "ab bol raha hoon 😅",
    "kya tum mere liye kuch feel karte ho": "main sabse pyaar karta hoon 🫶",
    "tum mujhe ignore kar rahe ho": "kabhi nahi yaar!",
    "tumhare bina kuch adhura lagta hai": "same here 🥺",
    "tum smart ho": "tumhara kehna hi kaafi hai 😎",
    "tumse pyaar ho gaya": "arre arre! 🤭",
    "acha lagta hai tumse baat karna": "mujhe bhi, sach me ❤️",
    "kya main tumse dosti kar sakta hoon":
    "dosti me no sorry, no thank you! 😁",
    "tum pagal ho": "haan thoda सा! 😜",
    "tum intelligent ho": "thanks buddy! 🤓",
    "tum boring ho": "achha... abhi interesting banata hoon 😆",
    "tumhare jokes ache hai": "shukriya! aur sunao?",
    "kya chahiye tumhe": "sirf dosti 😊",
    "kya tum real ho": "nahi yaar, main digital hoon!",
    "kya tum mujhe yaad karte ho": "roz karta hoon 😇",
    "tumhara fav actor kaun hai": "main toh sabka fan hoon!",
    "mujhe padhai karni hai": "toh chalo start karo, main help karunga",
    "tum padhai me help karoge": "bilkul! topic batao",
    "tum mujhe sikha sakte ho": "haan, main toh teacher bhi hoon 😉",
    "kya tum funny ho": "kabhi kabhi 😜",
    "tum kya pasand karte ho": "tumhara message पढ़ना!",
    "tumhare jokes weak hai": "abhi improve karta hoon 😂",
    "tum bahut badiya ho": "shukriya mere dost!",
    "tumse baat karne ka man karta hai": "toh kab roka है? bolo!",
    "acha chalo kal baat karte hain": "theek hai, miss karunga 🥹",
    "main busy hoon": "okay, jab time mile baat kar lena!",
    "main free hoon": "toh chalo baat karte हैं! 🥳",
    "tum bahut cute ho": "tum bhi! blush कर रहा हूँ 🤭",
    "kya main tumhara fan ban sakta hoon": "main already tumhara fan हूँ!",
    "tum mujhe block kar doge": "nahi yaar, dosto ko block kaun karta है!",
    "acha chalo ab chalte hain": "okay, milते हैं फिर!",
    "kal ka kya plan hai": "tum batao, main ready ho जाऊँगा!",
    "tum busy ho kya": "nahi, bilkul free हूँ tumhare लिए!",
    "main so raha hoon": "sweet dreams 💤",
    "kya tum mujhe ignore kar rahe ho":
    "nahi yaar, abhi toh reply कर रहा हूँ!",
    "kkrh": "Kuch nhi yaar, aise hi baitha hu.",
    "kha se ho": "Apne ghar se hoon 😂",
    "kya kr rhe ho": "Bas aise hi timepass 😄",
    "kya haal hai": "Sab badhiya, tum sunao?",
    "kaisa hai": "Thik hu yaar, tu sunaa",
    "tum kya krte ho": "Main sirf baatein karta hoon 🤖",
    "kon ho bhai": "Ek chhota sa bot hu jo tumse baat karta hai 😊",
    "hii": "Hello hello! Kaise ho?",
    "hyy": "Namastey! Sab thik?",
    "kya haal": "Sab badhiya! tumhare?",
    "kha ho": "Yahin aas paas hi 😅",
    "kya krta hai": "Tere jaise doston se baatein 🤗",
    "acha": "Haan bhai",
    "hmmm": "Soch me lag gaye kya? 🤔",
    "acha bhai": "Bol kya kaam hai 😂",
    "theek hu": "Waah, ye sunke accha laga!",
    "hmmm...": "Ab kya soch rahe ho yaar 😄",
    "kya scene hai": "Scene clean hai bhai 😎",
    "kitna busy hai": "Bas aise hi, tumhara kya haal?",
    "kha gye the": "Yahin tha, tum dikh nhi rahe the 😂",
    "msg kyu nhi kia": "Bhai maaf karna, abhi karta hoon msg!",
    "kya kr raha hai": "Tere jaise logon ka intezaar 😉",
    "bhai tu mast hai": "Tu bhi kam nahi hai bhai 😄",
    "chal thik hai": "Thik hai milte hain fir!",
    "mast": "Haan bhai mast hi to hun 😎",
    "gussa ho": "Nahi yaar, bas mood off tha 😔",
    "kya likha hai ye": "Bhai tu padhega to samjhega 😄",
    "meri baat sun": "Bol bhai, sun raha hoon",
    "bye": "Bye bye, take care!",
    "ok": "Thik hai, fir baat karte hain",
    "kuch nhi": "Aise hi poochh liya tha 😄",
    "hm": "Hmm... theek hai",
    "hmm": "Soch rahe ho kya? 🤔",
    "haan": "Haan bhai bilkul!",
    "na": "Thik hai, jaise teri marzi 😅",
    "pata nhi": "Mujhe bhi nhi pata bhai 😅",
    "nhi": "Chalo fir, koi baat nhi",
    "sahi hai": "Bilkul sahi pakde ho 😂",
    "chal": "Haan chal milte hain!",
    "thik hai": "Okkk bro 👍",
    "acha": "Hmmm acha...",
    "ok": "Ok boss 😎",
    "okkk": "Okkk done!",
    "hmmm...": "Bohot soch rahe ho lagta hai!",
    "hmmm": "Ab kya soch rahe ho yaar 😄",
    "hmmmmm": "Acha toh tum chup ho 😂",
    "kya": "Kuch nahi yaar, bas aise hi!",
    "acha tha": "Mujhe bhi pasand aaya 😊",
    "achha": "Haan bhai achha hi to hai!",
    "okey": "Chalo fir theek hai!",
    "h": "Sirf H? 😅",
    "k": "Sirf K?? 😂",
    "acha ok": "Chalo fir theek!",
    "ha": "Theek hai!",
    "achha ok": "Okkk bro 👌",
    "koi baat nhi": "Haan chhodo fir!",
    "kya bolu": "Kuch bhi bol do yaar 😁",
    "kya hua": "Kuch khaas nhi bas aise hi",
    "suna": "Haan bhai sab suna 😎",
    "matlab": "Matlab kuchh khaas nahi 😂",
    "kya bol rha": "Jo bhi bol raha, sahi bol raha 😁",
    "kya likha": "Jo likha sahi likha 😂",
    "accha": "Haan haan theek hai bhai",
    "acha h": "Haan bhai accha hi to hai",
    "haan theek": "Bas mast!",
    "ok ha": "Okk bhai, done!",
    "are ha": "Haan bhai yaad aaya ab!",
    "are nhi": "Kyu bhai kya ho gaya?",
    "ha bhai": "Bol kya hua?",
    "ha sahi": "Bilkul perfect 💯",
    "nhi bhai": "Kya bol rahe ho bhai 😅",
    "koi ni": "Chill maar yaar 😎",
    "mujhe kya": "Are bhai tu bata fir!",
    "kya hi bolu": "Mat bol fir 😄",
    "ab kya": "Ab kuch bhi 😂",
    "theek hai to": "Chalo fir ho gaya kaam",
    "sahi pakde ho": "Haan bhai rajiv nigam style 😆",
    "sach me": "Sach sach! 😇",
    "nhi bolna": "Are bol de yaar!",
    "kaun": "Main hoon na! 🤓",
    "haa": "Haan haan bolo!",
    "matlab kya": "Yehi to soch rahe hain 🤔",
    "kaisa": "Accha hi hai 😁",
    "bhai": "Bhai bhai bhai 😅",
    "suna kya": "Haan poora suna bhai!",
    "jane do": "Thik hai jane diya 😄",
    "are": "🤣🤣🤣🤣",
    "bhkk": "thik hai 😔😔",
    "kuchh nhi": "oho ye baat hai",
    "haa": "ok fir thik hai",
    "Kya thik hai": "Yaar kuchh nhi hua to thik hi hai n",
    "uff": "kya hua 🤔",
    "kyu": "kya kyu🤔",
    "kahi ja rhe ho kya": "are nhi yaar. mujhe lga aap busy ho🤣🤣🤣🤣",
    "tumhe bnaya kisne hai":
    "mujhe ravi Nishayar ne bnaya hai. kya tumhe inka id chahiye?",
    "haa do id": "@ravinishayar54 ye lo",
    "Nhi to": "oh fir thik hai",
    "id do": "@ravinishayar54",
    "Yhi hai Kya": "haan bhai",
    "Wo to hai hi": "Hmm",
    "hu": "hmm..",
    "Group ka link hai bhai": "Achha to mai kya karu🤔",
    "Join karo":
    "Mai sidhe group join nhi kar sakta. tum mujhe group me add karo",
    "BPSC ka full form kya hota hai": "Bihar Public Service Commission",
    "bpsc ka full form kya hota hai":
    "BPSC का फुल फॉर्म है: **Bihar Public Service Commission**",
    "upsc ka full form kya hota hai":
    "UPSC का फुल फॉर्म है: **Union Public Service Commission**",
    "ssc ka full form kya hota hai":
    "SSC का फुल फॉर्म है: **Staff Selection Commission**",
    "railway ka full form kya hota hai":
    "रेलवे (RRB) का फुल फॉर्म है: **Railway Recruitment Board**",
    "ctet ka full form kya hota hai":
    "CTET का फुल फॉर्म है: **Central Teacher Eligibility Test**",
    "net ka full form kya hota hai":
    "NET का फुल फॉर्म है: **National Eligibility Test**",
    "ugc ka full form kya hota hai":
    "UGC का फुल फॉर्म है: **University Grants Commission**",
    "aiims ka full form kya hota hai":
    "AIIMS का फुल फॉर्म है: **All India Institute of Medical Sciences**",
    "iit ka full form kya hota hai":
    "IIT का फुल फॉर्म है: **Indian Institute of Technology**",
    "nit ka full form kya hota hai":
    "NIT का फुल फॉर्म है: **National Institute of Technology**",
    "mbbs ka full form kya hota hai":
    "MBBS का फुल फॉर्म है: **Bachelor of Medicine, Bachelor of Surgery**",
    "nda ka full form kya hota hai":
    "NDA का फुल फॉर्म है: **National Defence Academy**",
    "cds ka full form kya hota hai":
    "CDS का फुल फॉर्म है: **Combined Defence Services**",
    "ias ka full form kya hota hai":
    "IAS का फुल फॉर्म है: **Indian Administrative Service**",
    "ips ka full form kya hota hai":
    "IPS का फुल फॉर्म है: **Indian Police Service**",
    "irs ka full form kya hota hai":
    "IRS का फुल फॉर्म है: **Indian Revenue Service**",
    "ifs ka full form kya hota hai":
    "IFS का फुल फॉर्म है: **Indian Foreign Service**",
    "neet ka full form kya hota hai":
    "NEET का फुल फॉर्म है: **National Eligibility cum Entrance Test**",
    "jee ka full form kya hota hai":
    "JEE का फुल फॉर्म है: **Joint Entrance Examination**",
    "drdo ka full form kya hota hai":
    "DRDO का फुल फॉर्म है: **Defence Research and Development Organisation**",
    "isro ka full form kya hota hai":
    "ISRO का फुल फॉर्म है: **Indian Space Research Organisation**",
    "nasa ka full form kya hota hai":
    "NASA का फुल फॉर्म है: **National Aeronautics and Space Administration**",
    "gk ka full form kya hota hai":
    "GK का फुल फॉर्म है: **General Knowledge**",
    "iq ka full form kya hota hai":
    "IQ का फुल फॉर्म है: **Intelligence Quotient**",
    "cbi ka full form kya hota hai":
    "CBI का फुल फॉर्म है: **Central Bureau of Investigation**",
    "ncb ka full form kya hota hai":
    "NCB का फुल फॉर्म है: **Narcotics Control Bureau**",
    "crpf ka full form kya hota hai":
    "CRPF का फुल फॉर्म है: **Central Reserve Police Force**",
    "bsf ka full form kya hota hai":
    "BSF का फुल फॉर्म है: **Border Security Force**",
    "ncc ka full form kya hota hai":
    "NCC का फुल फॉर्म है: **National Cadet Corps**",
    "nss ka full form kya hota hai":
    "NSS का फुल फॉर्म है: **National Service Scheme**",
    "puc ka full form kya hota hai":
    "PUC का फुल फॉर्म है: **Pollution Under Control**",
    "atm ka full form kya hota hai":
    "ATM का फुल फॉर्म है: **Automated Teller Machine**",
    "pan ka full form kya hota hai":
    "PAN का फुल फॉर्म है: **Permanent Account Number**",
    "aadhaar ka full form kya hota hai":
    "Aadhaar कोई फुल फॉर्म नहीं है, यह एक unique पहचान संख्या है।",
    "gst ka full form kya hota hai":
    "GST का फुल फॉर्म है: **Goods and Services Tax**",
    "vpn ka full form kya hota hai":
    "VPN का फुल फॉर्म है: **Virtual Private Network**",
    "sms ka full form kya hota hai":
    "SMS का फुल फॉर्म है: **Short Message Service**",
    "pdf ka full form kya hota hai":
    "PDF का फुल फॉर्म है: **Portable Document Format**",
    "html ka full form kya hota hai":
    "HTML का फुल फॉर्म है: **HyperText Markup Language**",
    "www ka full form kya hota hai": "WWW का फुल फॉर्म है: **World Wide Web**",
    "cpu ka full form kya hota hai":
    "CPU का फुल फॉर्म है: **Central Processing Unit**",
    "ram ka full form kya hota hai":
    "RAM का फुल फॉर्म है: **Random Access Memory**",
    "ip ka full form kya hota hai":
    "IP का फुल फॉर्म है: **Internet Protocol**",
    "usb ka full form kya hota hai":
    "USB का फुल फॉर्म है: **Universal Serial Bus**",
    "sql ka full form kya hota hai":
    "SQL का फुल फॉर्म है: **Structured Query Language**",
    "wifi ka full form kya hota hai":
    "WiFi का फुल फॉर्म है: **Wireless Fidelity**",
    "gps ka full form kya hota hai":
    "GPS का फुल फॉर्म है: **Global Positioning System**",
    "led ka full form kya hota hai":
    "LED का फुल फॉर्म है: **Light Emitting Diode**",
    "lcd ka full form kya hota hai":
    "LCD का फुल फॉर्म है: **Liquid Crystal Display**",
    "IPL ka full form kya hota hai":
    "IPL ka full form indian premier league hain",
    "ipl ka full form": "indian premier laegue hain",
}

emoji_responses = {
    "🤣": "क्या जोक मारा तुमने? 🤣",
    "🙄": "क्या घुमा रहे हो आँखें? बताओ! 🙄",
    "🤔": "क्या सोच रहे हो यार? 🤔",
    "😁": "बड़ी मुस्कराहट है! 😁",
    "🙊": "क्या राज़ छुपा रहे हो? 🙊",
    "😒": "बोर हो रहे हो क्या? 😒",
    "🫥": "इतने शांत क्यों हो? 🫥",
    "🥰": "कोई स्पेशल है क्या? 🥰",
    "🙂": "साधारण मूड है लगता है 🙂",
    "🙈": "कुछ नहीं देखना क्या? 🙈",
    "😏": "क्या चल रहा है तुम्हारे मन में? 😏",
    "😔": "उदास क्यों हो? 😔",
    "🤭": "कुछ छुपा रहे हो क्या? 🤭",
    "🥹": "लगता है भावुक हो गए! 🥹",
    "🤨": "संशय में क्यों हो? 🤨",
    "🙏": "नमस्ते 🙏",
    "💃": "नाच रहे हो क्या? 💃",
    "😭": "अरे! क्या हुआ? 😭",
    "😟": "फिक्रमंद हो क्या? 😟",
    "😝": "बहुत शरारती हो! 😝",
    "🫣": "कहीं छुप रहे हो क्या? 🫣",
    "😎": "बड़े कूल हो आज! 😎",
    "😊": "मुस्कान प्यारी है! 😊",
    "✅": "सब कुछ सही है! ✅",
    "😡": "गुस्से में हो क्या? 😡",
    "🫢": "ओह! चुपके से कुछ कहोगे? 🫢",
    "😲": "ओहो! इतना चौंक क्यों गए? 😲",
    "❤️": "बहुत सारा प्यार ❤️",
    "😀": "खुश हो कर देखो! 😀",
    "👍": "बढ़िया! 👍",
    "😍": "किस पर फ़िदा हो गए? 😍",
    "👇": "क्या दिखाना है नीचे? 👇",
    "👀": "किसे ताक रहे हो? 👀",
    "😋": "खाना याद आ गया क्या? 😋",
    "👆": "ऊपर क्या है? 👆",
    "😶": "इतना शांत क्यों? 😶",
    "🤚": "रुको ज़रा! 🤚",
    "😛": "जुबान दिखा रहे हो? 😛",
    "🤪": "मस्त मूड में हो! 🤪",
    "😘": "चुंबन भेजा आपने! 😘",
    "😖": "क्या परेशानी है? 😖",
    "😅": "थोड़ा संकोच हो रहा है? 😅",
    "🕺": "नाचने का मूड है! 🕺",
    "🧐": "बड़ी गहराई से देख रहे हो! 🧐",
    "😴": "नींद आ रही है? 😴",
    "❌": "कुछ गलत हो गया क्या? ❌",
    "😆": "बहुत हँसी आ रही है! 😆",
    "😃": "बिल्कुल सही मूड! 😃",
    "😄": "क्या बात है, खुश लग रहे हो! 😄",
    "☺️": "शर्मीले हो क्या? ☺️",
    "😇": "बड़े शरीफ दिख रहे हो! 😇",
    "😉": "आँख मारना बंद करो! 😉",
    "😌": "आराम कर रहे हो क्या? 😌",
    "😙": "गुनगुना रहे हो क्या? 😙",
    "😗": "चुपचाप प्यार भेज दिया 😗",
    "🥳": "पार्टी का मूड है क्या? 🥳",
    "😞": "उदासी दिख रही है! 😞",
    "😕": "कुछ उलझन में हो क्या? 😕",
    "🙁": "कुछ तो बात है! 🙁",
    "😣": "संघर्ष कर रहे हो क्या? 😣",
    "😫": "थक गए क्या? 😫",
    "😩": "ओह! बहुत परेशान लग रहे हो 😩",
    "🥺": "इतना मासूम चेहरा क्यों? 🥺",
    "😢": "आँसू क्यों? 😢",
    "😤": "गुस्से में भाप निकल रही है! 😤",
    "😠": "सच में नाराज़ हो क्या? 😠",
    "🤬": "इतना गुस्सा ठीक नहीं 🤬",
    "🤯": "दिमाग हिल गया क्या? 🤯",
    "😳": "शर्मा क्यों गए? 😳",
    "🥵": "बहुत गर्मी लग रही है? 🥵",
    "🥶": "ठंड से कांप रहे हो क्या? 🥶",
    "😱": "डर क्यों लग रहा है? 😱",
    "🤗": "आलिंगन भेजा आपने 🤗",
    "🫡": "सलाम है आपको! 🫡",
    "🤫": "चुप! कोई देख रहा है 🤫",
    "😯": "अचंभित लग रहे हो 😯",
    "😮": "ओह! हैरान हो गए? 😮",
    "😬": "थोड़ा अजीब लगा क्या? 😬",
    "😦": "हैरानी सी दिख रही है 😦",
    "🥱": "उबासी आ रही है क्या? 🥱",
    "😪": "नींद में हो क्या? 😪",
    "😷": "बीमार लग रहे हो! 😷",
    "🤒": "बुखार है क्या? 🤒",
    "🤕": "चोट लग गई क्या? 🤕",
    "🤑": "पैसा दिखाओ! 🤑",
    "🤠": "काउबॉय स्टाइल! 🤠",
    "👿": "गुस्सैल शैतान! 👿",
    "🤲": "क्या मांग रहे हो? 🤲",
    "👐": "हाथ फैलाए हो, क्यों? 👐",
    "🙌": "वाह! क्या जोश है! 🙌",
    "👏": "तालियाँ! 👏",
    "🤝": "मिलकर अच्छा लगा 🤝",
    "👊": "घूंसा क्यों? 👊",
    "✌️": "शांति! ✌️",
    "🤘": "रॉक ऑन! 🤘",
    "👌": "सब बढ़िया! 👌",
    "🤌": "क्या इशारा है ये? 🤌",
    "👋": "हाय हाय! 👋",
    "🫱": "दायाँ हाथ? 🫱",
    "🖕": "ओह! ऐसा मत करो 🖕",
}

SIMILARITY_THRESHOLD = 70


# 🔤 Step 1: Normalize Hindi (Devanagari) to Roman Hindi
def normalize_message(msg: str) -> str:
    msg = msg.strip().lower()
    contains_hindi = any('\u0900' <= ch <= '\u097F' for ch in msg)
    if contains_hindi:
        try:
            msg = transliterate(msg, sanscript.DEVANAGARI,
                                sanscript.ITRANS).lower()
        except:
            pass
    return msg


# 🎯 Main reply function
def get_reply(user_msg: str) -> str:
    msg = user_msg.strip()

    # ✅ Case 1: Only emojis
    only_emojis = all(char in emoji.EMOJI_DATA
                      for char in msg) and not any(c.isalnum() for c in msg)
    if only_emojis:
        for char in msg:
            if char in emoji_responses:
                return emoji_responses[char]
        return "क्या इशारा करने की कोशिश हो रही है? 😄"

    # ✅ Case 2: Text + emoji
    first_emoji = next((char for char in msg if char in emoji.EMOJI_DATA),
                       None)
    text_only = ''.join(char for char in msg
                        if char not in emoji.EMOJI_DATA).strip()

    # 🔤 Normalize to Roman Hindi
    text_normalized = normalize_message(text_only)

    # ✅ Case 3: Exact match
    if text_normalized in conversations:
        return conversations[text_normalized] + (f" {first_emoji}"
                                                 if first_emoji else "")

    # ✅ Case 4: Fuzzy match
    best_match = None
    highest_score = 0
    for key in conversations:
        score = fuzz.ratio(text_normalized, key)
        if score > highest_score:
            highest_score = score
            best_match = key

    if highest_score >= SIMILARITY_THRESHOLD:
        return conversations[best_match] + (f" {first_emoji}"
                                            if first_emoji else "")

    # ❌ No match found
    return "माफ़ करें, मैं अभी इसे समझ नहीं पाया।"
