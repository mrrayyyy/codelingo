"""Small editorial seed lexicon, not a comprehensive CEFR authority.

Definitions are authored for this project. Every level is labeled an estimate.
Replace this adapter/data with a licensed, calibrated corpus for production.
"""
LEXICON: dict[str, tuple[str, str, str]] = {
    "authenticate": ("B2", "Verify the identity of a user or service.", "/ɔːˈθentɪkeɪt/"),
    "authentication": ("B2", "The process of verifying who a user or service is.", "/ɔːˌθentɪˈkeɪʃən/"),
    "authorization": ("B2", "Permission to access a resource or perform an action.", "/ˌɔːθəraɪˈzeɪʃən/"),
    "permission": ("B1", "The right to access something or carry out an action.", "/pəˈmɪʃən/"),
    "validate": ("B2", "Check that data meets the expected rules.", "/ˈvælɪdeɪt/"),
    "validation": ("B2", "The process of checking data against a set of rules.", "/ˌvælɪˈdeɪʃən/"),
    "retrieve": ("B2", "Get information back from a place where it is stored.", "/rɪˈtriːv/"),
    "persist": ("B2", "Keep data available after the current operation ends.", "/pəˈsɪst/"),
    "cache": ("B2", "Store a copy of data so it can be accessed more quickly.", "/kæʃ/"),
    "request": ("B1", "A message asking a service to provide data or perform an action.", "/rɪˈkwest/"),
    "response": ("B1", "The result a service sends back after receiving a request.", "/rɪˈspɒns/"),
    "resolve": ("B2", "Find an answer to a problem or finish an asynchronous operation.", "/rɪˈzɒlv/"),
    "handle": ("B1", "Deal with a situation or process an event.", "/ˈhændəl/"),
    "implement": ("B2", "Put a design or plan into working code.", "/ˈɪmplɪment/"),
    "dependency": ("B2", "A component that another component needs in order to work.", "/dɪˈpendənsi/"),
    "deploy": ("B2", "Make software available in its intended environment.", "/dɪˈplɔɪ/"),
    "configuration": ("B2", "The settings that control how a system behaves.", "/kənˌfɪɡəˈreɪʃən/"),
    "retry": ("B1", "Try an operation again after it has failed.", "/ˌriːˈtraɪ/"),
    "reliable": ("B1", "Able to work correctly and consistently.", "/rɪˈlaɪəbəl/"),
    "expire": ("B2", "Stop being valid after a specified time.", "/ɪkˈspaɪə/"),
    "credential": ("B2", "Information used to prove identity when accessing a system.", "/krɪˈdenʃəl/"),
    "repository": ("B2", "A place where project files and their history are managed.", "/rɪˈpɒzɪtəri/"),
    "transaction": ("B2", "A group of data operations treated as a single unit.", "/trænˈzækʃən/"),
    "rollback": ("B2", "Restore a system or transaction to an earlier state.", "/ˈrəʊlbæk/"),
    "assertion": ("B2", "A check that a condition expected by a program is true.", "/əˈsɜːʃən/"),
    "coverage": ("B2", "The extent to which tests exercise the behavior of a program.", "/ˈkʌvərɪdʒ/"),
    "deprecated": ("B2", "Discouraged from use because a better replacement is available.", "/ˈdeprəkeɪtɪd/"),
    "concurrent": ("B2", "Taking place during overlapping periods of time.", "/kənˈkʌrənt/"),
    "enqueue": ("B2", "Add an item to a queue for later processing.", None),
    "middleware": ("B2", "Software that processes requests between application components.", None),
    "refresh": ("B1", "Obtain a new or updated version of data or a token.", "/rɪˈfreʃ/"),
    "session": ("B1", "A period of interaction between a user and a service.", "/ˈseʃən/"),
    "resource": ("B1", "Data or a service that can be accessed or used.", "/rɪˈzɔːs/"),
}

A1_WORDS = set("able about above across action add after again all also always am an and any are around as ask at away back bad be because become before begin best better big book both bring build busy but buy by call can change check child city clear close code come common company complete computer could count create current daily data day delete different do document dog down each easy else end enough even every example far fast feel few file find first five fix follow food for form four free friend from full function get give go good great group grow had half happen happy hard has have he head hello help her here high him his home hour how i if important in include information input inside into is it its job just keep key know language large last late later learn leave left let life like line list little live local long look lot low made make man many may me mean message might minute miss model money month more most move much must my name need never new next nice no not now number of off often old on once one only open or order other our out output over own page part people person place plan play please point problem program project public put question quick read ready real really remove result return right room run said same save say school second see seem send set she should show side simple since small so some something sometimes soon sound start state stay step still stop store string student such system table take talk task tell test text than thank that the their them then there these they thing think third this those three through time to today together too top try two type under understand up update us use user usual value very view wait walk want was watch water way we week well were what when where which while white who why will with word work world would write wrong year yes yet you young your".split())

KEYWORDS = set("abstract any async await boolean break case catch char class const continue debugger def default del do double elif else enum except export extends false final finally float for from global goto if implements import in instanceof int interface lambda len long map namespace native new nil none nonlocal null object package pass private protected public raise range readonly record return select self short static str struct super switch synchronized this throw throws true try type typeof undefined var void volatile while with yield bytes console println print fmt error err args kwargs id url api http https json sql html css jsx tsx utf uuid sha eof div span href src px rem em todo fixme eslint noqa typevar object promise unimplemented".split())

TOPICS: dict[str, set[str]] = {
    "auth": set("authenticate authentication authorization permission credential token session expire refresh identity access".split()),
    "database": set("persist database transaction rollback query record migration schema storage retrieve cache".split()),
    "networking": set("request response network retry endpoint timeout connection socket reliable middleware".split()),
    "testing": set("assertion coverage fixture mock test validate validation".split()),
    "UI": set("render component button layout interface input display navigation".split()),
    "workflow": set("deploy repository implement dependency configuration resolve concurrent enqueue deprecated".split()),
}
