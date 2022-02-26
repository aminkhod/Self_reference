#Hier wird die Traitliste vorgegeben, die Position, an der das Wort steht, entspricht der Itemnummer (nicht unbedingt der Trialnummer oder TrialID im Experiment, denn die ist abhängig von der Versuchsbedingung)


traits <- c("collector", "trendy", "strategist", "tough", "exuberant", "granny", "commentator", "compromiser", "sincere", "happy", "responsible", "truthful", "considerate", "humane", "intelligent", "ethical", "changeable", "daydreamer","serious", "geeky", "talkative", "methodical", "streetwise", "nonchalant", "cheerful", "nice", "generous", "cooperative", "helpful", "grateful", "sympathetic", "gracious", "wealthy", "parental", "daring", "informal", "subtle", "systematic", "undergraduate", "conventional", "reliable", "wise", "positive", "thoughtful", "admirable")



#dies ist Testcode, der Spielantworten erzeugt, um zu schauen, ob der Code funktioniert, darum ist er auskommentiert

#df <- data.frame(matrix(nrow=5, ncol=5))
#colnames(df) <- c("VP","Recall01","Recall02","Recall03","Recall04")

#df$VP <- 1:5

#df$Recall01 <- c("admirable", "strategist", "Pferd", "Katze", "")
#df$Recall02 <- c("responsible", "granny", "humane", "exuberant", "")
#df$Recall03 <- c("geeky", "generous", "subtle", "cooperative", "nonchalant")
#df$Recall04 <- c("undergraduate", "", "sincere", "sincere", "sympathetic")



#hier muss - statt der Spieldaten- der Dataframe aus SPSS eingelesen werden. Die Recallvariablen 1-9 haben führende Nullen bekommen und sind nun alle lowercase


#Jetzt wird für jede Recall-Variable geschaut, ob und welches (das wievielte in der liste) Item erinnert wurde. Leere Felder bekommen eine Null, ein Feld mit Inhalt, das kein Match ist, muss von Hand überprüft werden, und bekommt eine 99


df$Hit01 <- match(df$Recall01, traits, nomatch = 99)
df$Hit01[(df$Hit01==99)&(df$Recall01=="")] <- 0


df$Hit02 <- match(df$Recall02, traits, nomatch = 99)
df$Hit02[(df$Hit02==99)&(df$Recall02=="")] <- 0


df$Hit03 <- match(df$Recall03, traits, nomatch = 99)
df$Hit03[(df$Hit03==99)&(df$Recall03=="")] <- 0


df$Hit04 <- match(df$Recall04, traits, nomatch = 99)
df$Hit04[(df$Hit04==99)&(df$Recall04=="")] <- 0



View(df)