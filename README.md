Verse Entities
==============

This project contains Python module that simplify implementation of Verse client. It contains several class of basic Verse entities:

* VerseSession
* VerseNode
* VerseTagGroup
* VerseTag
* VerseLayer

These classes could be used for implementation custom subclasees.

If you want to share some data on Verse server, then simple Verse client could look like this:

```python

import versentities as vrsent

def main():
    """
    Function with main never ending verse loop
    """
    session = vrsent.VerseSession()

    node = vrsent.VerseNode(session)
    tg = vrsent.VerseTagGroup(node)
    tag = vrsent.VerseTag(tg)
    tag.value = (10,)

    while(session.state != 'DISCONNECTED'):
        session.callback_update()
        time.sleep(1.0/session.fps)

if __name__ == '__main__':
	main()
```