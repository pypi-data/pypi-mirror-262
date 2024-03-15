from toolboxv2 import App, AppArgs, Spinner, tbef

from toolboxv2.utils import show_console

NAME = "mbgr"


# scraping :

# Emails
# Gmail MarkinHausmanns@gmail.com & Drrking883@gmail.com

def get_gmail_msg_tldr(app):
    gmail_msg = app.run_any(tbef.GMAILPROVIDER.SEARCH_MESSAGES, service=gmail_service_dr, query="TLDR")
    print(gmail_msg)
    # for msg in gmail_msg:
    _new_m = app.run_any(tbef.GMAILPROVIDER.READ_MESSAGE, service=gmail_service_dr, message=gmail_msg[0])
    print("New message:", _new_m)
    return _new_m, gmail_msg[0]


# and tuMail

# Uni Data Isis

# News Data
# ----------------------

# workflow :

# add event (read day plan ->
# collecting Email & uni & news data Present them in a md file and with a news reporter agent (verbal)

# ----------------------
# perma active :

# web ui
# isaa clip withe ask question verbal + data from day
# scrape web pages
# ----------------------
gmail_service_mh = None
gmail_service_dr = None


def run(app: App, args: AppArgs):
    global gmail_service_dr, gmail_service_mh
    from toolboxv2.mods.SchedulerManager import Tools as SM
    # setup runner
    show_console(True)
    # gmail_service_mh = app.run_any(tbef.GMAILPROVIDER.GMAIL_AUTHENTICATE, name="0")
    # gmail_service_dr = app.run_any(tbef.GMAILPROVIDER.GMAIL_AUTHENTICATE, name="1")
    # uni_mail_service = app.run_any(tbef.GMAILPROVIDER.LOG_IN, username="Kinr3@tu-berlin.de", password="3170mm3170M!")

    #bk_ankündigungen = "https://isis.tu-berlin.de/mod/forum/view.php?id=1669195"
#
    #daat = get_text_from_urls_play(bk_ankündigungen)[1]()

    #print("WEB DATA", daat, )

    with Spinner("Config runner setup Scheduler"):
        pass
        # scheduler: SM = app.get_mod("SchedulerManager")

        # app.run_any(tbef.SCHEDULERMANAGER.ADD,
        #             job_data={
        #                 "job_id": "job-example_basic",
        #                 "second": 20,
        #                 # "func": example_basic,
        #                 "job": None,
        #                 "time_passer": None,
        #                 "object_name": "tb_job_fuction",
        #                 "receive_job": False,
        #                 "save": False,
        #                 "max_live": False
        #             })
    pass
