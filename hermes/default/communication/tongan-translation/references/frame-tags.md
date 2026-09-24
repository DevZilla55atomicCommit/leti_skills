# Tongan Translation — Frame Tags Quick Reference

Extracted from `translate-pack.json` (lea-faka-tonga course). These are the **only valid frame tags** — inventing one is a hard error.

## Allowed Frames (Tier-1 Certified)

Frames with ≥3 verified log examples OR buildable by the live grammar-graph engine:

### Core Sentence Types
| Frame | Section | Template |
|-------|---------|----------|
| `statement` | §1 | `[tense_marker] + [pronoun] + [preposed_modifier] + [verb]` |
| `noun_subject` | §14 | `[tense_marker_ns] + [verb_ns] + [modifier_ns]` |
| `transitive_statement` | §16 | `[tense_marker_tr] + [verb_tr] + [object_phrase] + [agent_phrase]` |
| `experiencer` | §15 | `[tense_marker_exp] + [verb_experiencer] + [prep_pronoun]` |
| `location_state` | §2 | `[tense_marker_loc] + [pronoun_loc] + [preposition_i_fixed] + [place]` |

### Ko Constructions
| Frame | Section | Template |
|-------|---------|----------|
| `ko_identification` | §9 | `[ko_e_fixed] + [noun_ko] + [demonstrative]` |
| `ko_question_what` | §11 | `[ko_e_ha_fixed] + [demonstrative]` |
| `ko_question_who` | §12 | `[ko_hai_fixed] + [tense_marker_kohai] + [verb_kohai]` |
| `ko_question_where` | §13 | `[ko_fe_fixed] + [focus_and_name]` |
| `ko_equational` | §21 | `[ko_e_equational] + [equational_noun] + [modifier_eq] + [equational_subject]` |
| `ko_negation` | §10 | `[ko_neg_prefix] + [predicate_noun] + [subject_ko]` |
| `cleft_emphatic` | §19 | `[ko_emphatic] + [subject_phrase] + [tense_marker_cleft] + [pronoun_relative] + [verb_cleft]` |

### Negation
| Frame | Section | Template |
|-------|---------|----------|
| `negation` | §7 | `[tense_marker_neg] + [negation_word] + [neg_connector] + [pronoun_neg] + [preposed_modifier] + [verb]` |
| `negation_impersonal` | §8 | `[tense_marker_neg_imp] + [negation_word_imp] + [imp_connector] + [verb_weather]` |
| `existential` | §32 | `[existential_head] + [existential_noun]` |

### Commands & Suggestions
| Frame | Section | Template |
|-------|---------|----------|
| `command` | §3 | `[command_verb]` |
| `command_plural` | §4 | `[imperative_mou] + [command_verb_plural]` |
| `prohibition` | §5 | `[prohibition_marker] + [prohibition_pronoun] + [prohibition_verb]` |
| `suggestion` | §6 | `[suggestion_pronoun] + [verb]` |

### Possessive
| Frame | Section | Template |
|-------|---------|----------|
| `possessive_phrase` | §22 | `[possessive_pronoun] + [possessive_head_noun]` |
| `possessive_phrase_name` | §22 | `[possessor_preposition] + [possessor_name]` |
| `prep_with_possessive` | §22 | `[preposition_possessive] + [possessive_pronoun] + [possessive_head_noun]` |
| `predicative_possessive` | §40 | `[predicative_possessive_head] + [postposed_possessive] + [predicative_poss_subject]` |
| `have_construction` | §36 | `[have_head] + [possessive_pronoun] + [possessive_head_noun]` |

### Obligation / Permission / Optative
| Frame | Section | Template |
|-------|---------|----------|
| `obligation_should` | §28 | `[totonu_phrase] + [obligation_pronoun] + [verb]` |
| `obligation_must` | §28 | `[pau_phrase] + [obligation_pronoun] + [verb]` |
| `permission_tuku_ke` | §34 | `[tuku_ke_phrase] + [obligation_pronoun] + [verb]` |
| `optative_ofa_ke` | §34 | `[ofa_ke_phrase] + [obligation_pronoun] + [verb]` |

### Benefactive
| Frame | Section | Template |
|-------|---------|----------|
| `benefactive_name` | §25 | `[benefactive_preposition_ma] + [possessor_name]` |
| `benefactive_pronoun` | §25 | `[benefactive_pronoun_fused]` |

### Multi-Clause Connectors
| Frame | Section | Template |
|-------|---------|----------|
| `pea_second_clause` | §17 | `[clause_connector_pea] + [tense_marker] + [pronoun] + [preposed_modifier] + [verb]` |
| `contrast_clause_kae` | §17 | `[clause_connector_kae] + [verb_ns] + [modifier_ns]` |
| `reason_clause_he` | §25 | `[clause_connector_he] + [tense_marker] + [pronoun] + [preposed_modifier] + [verb]` |
| `purpose_bare_verb` | §25 | `[subordinator_ke_purpose] + [verb]` |
| `reason_clause_koeuhi_ke` | §25 | `[subordinator_koeuhi_ke] + [verb]` |
| `serial_clause` | §17 | `[clause_connector_o] + [verb]` |

### Advanced (Newer Additions)
| Frame | Section | Template |
|-------|---------|----------|
| `relative_clause` | §35 | `[relative_clause_tense] + [pronoun] + [preposed_modifier] + [verb]` |

---

## ⚠ Permanent Escalate Frames (Never Answer)

| Frame | Reason |
|-------|--------|
| `bare_clause_juxtaposition` | Always escalate |
| `conditional_clause` | Always escalate |
| `ka_conditional` | Always escalate |
| `ka_ne_counterfactual` | Always escalate |
| `subordinator_kapau` | Always escalate |
| `reported_speech_pehē` | Always escalate |
| `reported_speech_tui` | Always escalate |
| `reportative_tokua` | Always escalate |
| `exclamatory_ko_ka` | Always escalate |
| `exclamatory_me_a` | Always escalate |
| `ko_progressive_action` | Always escalate |
| `ko_e_mea_ia` | Not yet certified |
| `cleft_equational` | Not yet certified |
| `ko_question` | Not yet certified |
| `ko_e_ha_ai` | Not yet certified |
| `intransitive_question` | Not yet certified |
| `me_a_e_fiha` | Not yet certified |
| `mole_ke_mama_o_denial` | Not yet certified |
| `ne_ine_i_explanation` | Not yet certified |
| `predicate_stative` | Not yet certified |
| `te'eki_ai_standalone` | Not yet certified |
| `time_telling` | Not yet certified |
| `verbal_negation` | Not yet certified |
| `urge_fai_mo_ke` | Not yet certified |
| `subordinator_ke` | Not yet certified |
| `subordinator_koe'uhi` | Not yet certified |

---

## 5 Marker Disambiguators

1. **te vs ke after 'ikai**
   - `'ikai te` + pronoun → `negation`
   - `'ikai ke` + bare verb / 'i ai → `negation_impersonal` / `existential`

2. **na'a vs na'e** (and te vs 'e for future)
   - `na'a` + pronoun; `na'e` + non-pronoun (negation, noun subject, existential)

3. **ka vs kae** (two words for "but")
   - `ka` before tense marker/pronoun; `kae` before verb/adjective

4. **e vs he** (definite article "the")
   - `he` after 'i, ki, mei; `e` elsewhere

5. **Aspect markers** (pre/post-verb)
   - Pre-verb: `toe` (again), `kei` (still), `'osi` (already), `te'eki` (not yet)
   - Post-verb: `leva` (immediately), `ai pē` (as always), frequency markers

---

## Possessive Class Quick Check

**185 nouns indexed.** If noun NOT in table → escalate.

Common a-class: `fānau` (children), `ngāue` (work), `me'akai` (food), `tamai` (father), `fa'ē` (mother), `tamasi'i` (son), `moa` (chicken), `talo` (taro), `kumala` (sweet potato), `kato` (basket), `koloa` (goods)

Common o-class: `fale` (house), `fonua` (land), `kai` (eat→food), `hoa` (mate/spouse), `kaume'a` (friend), `kolo` (village), `vaka` (boat), `loki` (room), `mohenga` (bed), `nima` (hand), `va'a` (branch), `hala` (road), `mafai` (authority)

Class-shifters (reading decides): `fala` (mat), `vala` (clothes), `hiva` (song), `niu` (coconut), `moli` (orange), `fusi` (banana), `kava`, `tohi` (writing), `tokoni` (help), `vai` (water)

---

## House Rules (10 Standing Rulings)

1. **2026-06-08** — `fiha` not `fīha` (how many)
2. **2026-06-08** — `lalanga` (verb) ≠ `lālanga` (noun)
3. **2026-06-08** — `'Ana` name spelling standardized
4. **2026-06-13** — `ha'u` never combines with `mai` → `Ha'u ki heni` / `Ha'u ange`
5. **2026-06-13** — `alu` accepted alongside plural `o` (spoken usage)
6. **2026-06-13** — `ū` and `ngaahi` both accepted
7. **2026-06-15** — Negative existential: teach FULL `'oku 'ikai ke 'i ai`; short form also valid
8. **2026-06-20** — Glossary sort ignores fakau'a (interfiles), no separate section
9. **2026-06-27** — Glottal stop = **fakau'a** (Tongan), not ʻokina (Hawaiian)
10. **2026-06-10** — Stress accent on te-family before ANY one-syllable pronoun: `Té u`, `Té ke`, `Na'á ku`, `ʻikai té`, `ʻoua té`, `te'eki té`, `ta'e té`

---

## When to Escalate

Set `"escalate": true` when:
- English needs idiom/phrasal verb resolution first
- >2 finite clauses
- Reported speech ("said that…") or counterfactual ("would have…")
- Possessed noun not in the 185-noun index
- Required frame is ⚠ or not on the list
- Any word you'd write is not verifiably real Tongan