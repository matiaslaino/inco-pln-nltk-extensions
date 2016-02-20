# coding=utf-8
__author__ = 'Matias Laino'

from inco.nlp.parse.tree.maltparser_tree_builder import MaltParserTreeBuilder

str = u"""+grup-verb_[
  grup-sp_[
    +prep_[
      +(En en SPS00 -)
    ]
    sn_[
      espec-ms_[
        +j-ms_[
          +(eel el DA0MS0 -)
        ]
      ]
      +grup-nom-ms_[
        +n-ms_[
          +(tramo tramo NCMS000 -)
        ]
      ]
      sp-de_[
        +(de de SPS00 -)
        sn_[
          +grup-nom-ms_[
            +w-ms_[
              +(Telefónica telefónica NP00000 -)
            ]
          ]
        ]
      ]
    ]
  ]
  sn_[
    espec-ms_[
      +indef-ms_[
        +(un uno DI0MS0 -)
      ]
    ]
    +grup-nom-ms_[
      +n-ms_[
        +(toro toro NCMS000 -)
      ]
      s-a-ms_[
        +parti-ms_[
          +(descolgado descolgar VMP00SM -)
        ]
      ]
    ]
  ]
  +verb_[
    vaux_[
      +(ha haber VAIP3S0 -)
    ]
    +parti_[
      +(creado crear VMP00SM -)
    ]
  ]
  sn_[
    +grup-nom-ms_[
      +n-ms_[
        +(peligro peligro NCMS000 -)
      ]
    ]
  ]
  grup-sp-inf_[
    +prep_[
      +(tras tras SPS00 -)
    ]
    grup-verb-inf_[
      +infinitiu_[
        +inf_[
          +forma-inf_[
            +(embestir embestir VMN0000 -)
          ]
        ]
      ]
      grup-sp_[
        +prep_[
          +(contra contra SPS00 -)
        ]
        sn_[
          espec-ms_[
            +indef-ms_[
              +(un uno DI0MS0 -)
            ]
          ]
          +grup-nom-ms_[
            +n-ms_[
              +(grupo grupo NCMS000 -)
            ]
          ]
          sp-de_[
            +(de de SPS00 -)
            sn_[
              +grup-nom-mp_[
                +n-mp_[
                  +(mozos mozo NCMP000 -)
                ]
              ]
            ]
          ]
        ]
      ]
    ]
  ]
  F-term_[
    +(. . Fp -)
  ]
]"""

#fp = FreeLingTreeBuilder()
#t = fp.build(str)
#print t

mp_str = u"""1 En en s SPS00 _ 10 MOD _ _
2 el el d DA0MS0 _ 3 SPEC _ _
3 tramo tramo n NCMS000 _ 1 COMP _ _
4 de de s SPS00 _ 3 MOD _ _
5 Telefónica NP00000 n NP00000 _ 4 COMP _ _
6 un un z Z _ 7 SPEC _ _
7 toro toro n NCMS000 _ 10 SUBJ _ _
8 descolgado descolgar v VMP00SM _ 7 MOD _ _
9 ha haber v VAIP3S0 _ 10 AUX _ _
10 creado crear v VMP00SM _ 0 ROOT _ _
11 peligro peligro n NCMS000 _ 10 SUBJ _ _
12 tras tras s SPS00 _ 10 MOD _ _
13 embestir embestir v VMN0000 _ 12 COMP _ _
14 contra contra s SPS00 _ 13 MOD _ _
15 un un z Z _ 16 SPEC _ _
16 grupo grupo n NCMS000 _ 14 COMP _ _
17 de de s SPS00 _ 16 COMP _ _
18 mozos mozo n NCMP000 _ 17 COMP _ _
19 . . f Fp _ 18 punct _ _"""

mpt = MaltParserTreeBuilder()
print mpt.build(mp_str)