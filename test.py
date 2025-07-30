index = survey.routines.select(
  'Ｐｌｅａｓｅ ｓｅｌｅｃｔ ｔｈｅ ｏｐｔｉｏｎｓ ｔｏ ｆｉｌｌ ｉｎ ｔｈｅ ｃｒｅｄｅｎｔｉａｌｓ:\n',
  options=options,
  focus_mark='> ',
  evade_color=survey.colors.basic('white'),
  insearch_color=survey.colors.basic('white'))