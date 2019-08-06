# daily_reddit_headlines

Stay updated with your favorite subreddits headlines using Google's Text-to-Speech (TTS) voice.

---

## Usage and Example

*Input:* 

```python main.py```

*Output:* 
```python
Hello Andrei...

Today's worldnews headlines are...

1. Top Climate Scientist Quits USDA, Accuses Trump Administration of Trying to Bury Research...

2. 'An Act of Terrorism': Mexico Plans Legal Action Against US After 6 Citizens Killed in El Paso Shooting: "Mexico would like to express its utmost, profound condemnation and rejection of this barbaric act," said Marcelo Ebrard, Mexico's Foreign Minister...

3. Hong Kong students and emigrants in Taiwan have been buying helmets, goggles, umbrellas, plastic wrap and Band-Aids in bulk and couriering them to pro-democracy protesters in Hong Kong....

Today's technology headlines are...

1. Libraries are fighting to preserve your right to borrow e-books...

2. Senators demand Google make contractors full-time employees after 6 months...

3. A defiant 8chan vowed to fight on, saying its 'heartbeat is strong.' Then a tech firm knocked it offline...

Today's MusicNews headlines are...

1. Special interview collaboration with hard rock bands Weapons of Anew and Messer...

2. Ed Sheeran breaks U2's record for highest-grossing tour ever...

3. ASAP Rocky Is Ordered Freed From Jail Pending Verdict in Assault Trial
```
---

## Installation

__Note:__ *This has only been tried and tested on Debian. This installation guide may not work exactly the same way on other operating systems.*

1. Install everything on the ```requirements.txt``` file.
```pip install -r requirements.txt```

2. Update the ```config.yml``` file with:
    1. Your name
    2. The URLs of your favorite subreddits (Default subreddits are ```r/worldnews```, ```r/technology```, and ```r/MusicNews```)
    3. The number of headlines you want for each subreddit (Default number is 3)
    4. Any useless messages you do not want to listen to (Default is the default statements from ```r/technology```)
    5. The language that the Google Text-to-Speech voice should have (Default is ```en``` for English)
    6. Your Reddit username
    7. Your Reddit password

You are set!

---

## Acknowledgements
* This project is powered by [gTTS](https://gtts.readthedocs.io/en/latest/) and the [Reddit API](https://www.reddit.com/dev/api).

---

## Contributors
* Andrei Biswas: axb6972@rit.edu

---

## License
```daily_reddit_headlines``` is under the MIT license.
