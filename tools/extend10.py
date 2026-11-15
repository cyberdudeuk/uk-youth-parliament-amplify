"""Tenth set of portal extensions: launch-blocker fixes to the pledge screen and the phone view (15 November 2026).

  pledge   The design's pledge text promised things the prototype does not do (D26): public sharing, a pledge wall,
           messaging defaults, a message on the day the petition comes back, a named adult confirming a pledge, and an
           unsourced autumn relaunch. Each is replaced with what is true: a pledge stays on this device and nothing is
           sent or collected. The name box is marked optional and says it is saved only on this device, and a
           "Clear my pledges from this device" button removes any pledges from the screen and from browser storage
           (D27: on a shared school computer the next person could otherwise see them). check_site S14 and S18 fail a
           build that brings any of it back.
"""

CLEAR_LOGIC = r'''  ampClearPledges() {
    const n = (this.state.userPledges || []).length;
    try {
      const raw = localStorage.getItem("amplify.portal.prefs");
      if (raw) { const p = JSON.parse(raw); delete p.userPledges; localStorage.setItem("amplify.portal.prefs", JSON.stringify(p)); }
    } catch (e) { /* storage unavailable or blocked: nothing was kept there */ }
    this.setState({ userPledges: [], pName: "", announce: n ? (n === 1 ? "Your pledge has" : "Your " + n + " pledges have") + " been cleared from this device." : "There were no pledges of yours on this device to clear." });
  }
  savePrefs(keys) {'''

LABEL_OLD = '''">Name or initials
                <input value="{{ pName }}" onChange="{{ setPName }}" placeholder="e.g. J. Okafor" '''
LABEL_NEW = '''">Name or initials (optional)
                <span id="amp-pname-hint" style="font-size: 12px; color: rgb(var(--ink-rgb) / 0.8);">Saved only on this device, never sent. Leave it blank to pledge as Anonymous.</span>
                <input value="{{ pName }}" onChange="{{ setPName }}" aria-describedby="amp-pname-hint" placeholder="e.g. JO, or leave blank" '''

PLEDGE_BTN = '''margin-top: 2px;">Pledge my signature</button>'''
CLEAR_BTN = ('''margin-top: 2px;">Pledge my signature</button>
              <button type="button" onClick="{{ clearPledges }}" style="border: 1px solid rgb(var(--film-rgb) / 0.3); border-radius: 999px; min-height: 44px; padding: 10px 18px; '''
             '''font-size: 13.5px; font-weight: 700; color: rgb(var(--ink-rgb)); background: transparent; cursor: pointer;">Clear my pledges from this device</button>''')

UNDER13_OLD = ("Under 13? A named adult confirms on your behalf. No pledge is shown publicly with a full name unless you are over 16. "
               "In this prototype a pledge is saved in your browser only: nothing is sent.")
UNDER13_NEW = ("Under 13? Ask a trusted adult before you pledge. Nothing is shown publicly: in this prototype a pledge is saved in this "
               "browser only and nothing is sent. On a shared or school computer, clear your pledges when you finish.")


def transforms():
    return [
        ("ext10-feed-1113", "D26: nothing is collected, so no one can be sent a message on the day the petition comes back",
         "It closed with 1,192 names and needed 10,000. Pledging means you get one message on the day it comes back.",
         "It closed with 1,192 names and needed 10,000. A pledge here stays on this device: nothing is collected or sent.", 1),
        ("ext10-feed-1418", "D26: no source says a relaunch is planned for the autumn term",
         "Closed at 1,192 of the 10,000 needed for a response. A relaunch is being planned for the autumn term; a pledge is a promise to sign in hour one,",
         "Closed at 1,192 of the 10,000 needed for a response. A pledge is a promise to sign any new petition in its first hour,", 1),
        ("ext10-safe-1418", "D26: the portal has no public sharing, no pledge wall and no messaging",
         "You are in 14\\u201318 mode. Public sharing is on, your first name and initial can appear on the pledge wall, and direct messaging to adults outside your school is off by default.",
         "You are in 14\\u201318 mode. Pledges stay on this device and nothing is sent: this prototype has no public pledge wall and no messaging.", 1),
        ("ext10-safe-1113", "D26: no adult confirms a pledge and nothing is shared to group chats; say what is true",
         "You are in under-13 mode. Sharing goes to group chats you are already in, your name is never shown publicly, and a named adult confirms any pledge for you.",
         "You are in under-13 mode. Pledges stay on this device and nothing is sent, so your name is never shown publicly. Ask a trusted adult before you share anything.", 1),
        ("ext10-pledge-note", "D26: no adult confirms a pledge, and no pledge is shown publicly at any age",
         UNDER13_OLD, UNDER13_NEW, 1),
        ("ext10-name-optional", "D27: the name is optional and stays on this device; say so where it is typed",
         LABEL_OLD, LABEL_NEW, 1),
        ("ext10-clear-button", "D27: a clearly labelled way to remove pledges from a shared computer",
         PLEDGE_BTN, CLEAR_BTN, 1),
        ("ext10-clear-logic", "D27: clearing removes the pledges from the screen and from browser storage, inside try/catch",
         "  savePrefs(keys) {", CLEAR_LOGIC, 1),
        ("ext10-clear-val", "D27: the button's handler joins renderVals",
         "        pName: \"\"\n      })),\n",
         "        pName: \"\"\n      })),\n      clearPledges: () => this.ampClearPledges(),\n", 1),
    ]
