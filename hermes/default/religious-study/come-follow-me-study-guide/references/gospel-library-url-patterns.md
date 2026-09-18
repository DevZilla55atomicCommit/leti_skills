# Gospel Library URL Patterns

## Base URL Structure
```
https://www.churchofjesuschrist.org/study/scriptures/ot/{book_path}/{chapter}?lang=eng[&id={verse}]
```

## Book Path Map (Old Testament)
| Book | Path | Example |
|------|------|---------|
| Genesis | gen | `/gen/3?lang=eng&id=4-5` |
| Exodus | ex | `/ex/20?lang=eng` |
| Leviticus | lev | `/lev/19?lang=eng&id=18` |
| Numbers | num | `/num/6?lang=eng&id=24-26` |
| Deuteronomy | deut | `/deut/6?lang=eng&id=5` |
| Joshua | josh | `/josh/1?lang=eng` |
| Judges | judg | `/judg/6?lang=eng` |
| Ruth | ruth | `/ruth/1?lang=eng` |
| 1 Samuel | 1-sam | `/1-sam/1?lang=eng` |
| 2 Samuel | 2-sam | `/2-sam/7?lang=eng` |
| 1 Kings | 1-kgs | `/1-kgs/3?lang=eng` |
| 2 Kings | 2-kgs | `/2-kgs/2?lang=eng` |
| 1 Chronicles | 1-chr | `/1-chr/1?lang=eng` |
| 2 Chronicles | 2-chr | `/2-chr/7?lang=eng` |
| Ezra | ezra | `/ezra/1?lang=eng` |
| Nehemiah | neh | `/neh/1?lang=eng` |
| Esther | esth | `/esth/1?lang=eng` |
| Job | job | `/job/1?lang=eng&id=1` |
| Psalms | ps | `/ps/23?lang=eng&id=1` |
| Proverbs | prov | `/prov/3?lang=eng&id=5-6` |
| Ecclesiastes | eccl | `/eccl/3?lang=eng&id=1` |
| Song of Solomon | song | `/song/1?lang=eng` |
| Isaiah | isa | `/isa/40?lang=eng&id=26` |
| Jeremiah | jer | `/jer/29?lang=eng&id=11` |
| Lamentations | lam | `/lam/3?lang=eng&id=22-23` |
| Ezekiel | ezek | `/ezek/36?lang=eng&id=26` |
| Daniel | dan | `/dan/3?lang=eng&id=17-18` |
| Hosea | hosea | `/hosea/6?lang=eng&id=1` |
| Joel | joel | `/joel/2?lang=eng&id=28-29` |
| Amos | amos | `/amos/5?lang=eng&id=24` |
| Obadiah | obad | `/obad/1?lang=eng` |
| Jonah | jonah | `/jonah/1?lang=eng` |
| Micah | micah | `/micah/6?lang=eng&id=8` |
| Nahum | nahum | `/nahum/1?lang=eng` |
| Habakkuk | hab | `/hab/2?lang=eng&id=4` |
| Zephaniah | zeph | `/zeph/3?lang=eng&id=17` |
| Haggai | hag | `/hag/2?lang=eng&id=4` |
| Zechariah | zech | `/zech/3?lang=eng&id=1` |
| Malachi | mal | `/mal/3?lang=eng&id=1` |

## Book Path Map (New Testament)
| Book | Path |
|------|------|
| Matthew | matt |
| Mark | mark |
| Luke | luke |
| John | jn |
| Acts | acts |
| Romans | rom |
| 1 Corinthians | 1-cor |
| 2 Corinthians | 2-cor |
| Galatians | gal |
| Ephesians | eph |
| Philippians | phil |
| Colossians | col |
| 1 Thessalonians | 1-thes |
| 2 Thessalonians | 2-thes |
| 1 Timothy | 1-tim |
| 2 Timothy | 2-tim |
| Titus | titus |
| Philemon | phlm |
| Hebrews | heb |
| James | james |
| 1 Peter | 1-pet |
| 2 Peter | 2-pet |
| 1 John | 1-jn |
| 2 John | 2-jn |
| 3 John | 3-jn |
| Jude | jude |
| Revelation | rev |

## Book Path Map (Book of Mormon)
| Book | Path |
|------|------|
| 1 Nephi | 1-ne |
| 2 Nephi | 2-ne |
| Jacob | jacob |
| Enos | enos |
| Jarom | jarom |
| Omni | omni |
| Words of Mormon | w-of-m |
| Mosiah | mosiah |
| Alma | alma |
| Helaman | hel |
| 3 Nephi | 3-ne |
| 4 Nephi | 4-ne |
| Mormon | morm |
| Ether | ether |
| Moroni | moro |

## Book Path Map (Doctrine & Covenants)
| Book | Path |
|------|------|
| D&C | dc |

## Book Path Map (Pearl of Great Price)
| Book | Path |
|------|------|
| Moses | moses |
| Abraham | abr |
| Joseph Smith—Matthew | js-m |
| Joseph Smith—History | js-h |
| Articles of Faith | a-of-f |

## URL Construction Rules
1. **Chapter only**: `/{path}/{chapter}?lang=eng`
2. **Chapter + verse**: `/{path}/{chapter}?lang=eng&id={verse}`
3. **Verse range**: Use en-dash (–) or hyphen (-): `id=1-3` or `id=1–3`
4. **Language**: Always include `?lang=eng`
5. **Encoding**: Use URL encoding for special characters

## Example URLs
- Job 1:1 → `https://www.churchofjesuschrist.org/study/scriptures/ot/job/1?lang=eng&id=1`
- Psalm 23:1 → `https://www.churchofjesuschrist.org/study/scriptures/ot/ps/23?lang=eng&id=1`
- D&C 45:3–5 → `https://www.churchofjesuschrist.org/study/scriptures/dc/45?lang=eng&id=3-5`
- 2 Nephi 2:11–13 → `https://www.churchofjesuschrist.org/study/scriptures/bofm/2-ne/2?lang=eng&id=11-13`
- Abraham 3:22–26 → `https://www.churchofjesuschrist.org/study/scriptures/pgp/abr/3?lang=eng&id=22-26`

## Notes
- Old Testament books use `/ot/` path
- New Testament books use `/nt/` path
- Book of Mormon books use `/bofm/` path
- Doctrine & Covenants uses `/dc/` path
- Pearl of Great Price uses `/pgp/` path
- The API automatically routes based on book path