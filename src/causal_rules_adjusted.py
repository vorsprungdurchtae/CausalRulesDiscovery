from data_prep_adjusted import read_prep_data
from action_rules_adjusted import actionDiscovery, interpretRules, get_unique_actions
from uplift_tree_adjusted import create_uplift_tree

data = 'pseudo_eventlog_final.csv'
df = read_prep_data(data)

consequent_col = 'NotCancelled'

st_col = ['BinnedDuration',
          'BinnedCompanion',
          'Accomodation',
          'Rating']

flex_col = ['Upgrade', 'Reschedule', 'CancellationFee']

uplift = []
r_list = []
rep_list = []
print("=================Start============================================\n")
print(f"Stable cols: {st_col}\nFlexible_cols: {flex_col}\n")
rules, length, rules_representation = actionDiscovery(df, st_col, flex_col, consequent_col)
uplift.extend(interpretRules(rules, length, rules_representation))
rep_list.extend(rules_representation)
r_list.extend(rules)
print("===============================Finish================================\n")

r_copy2 = get_unique_actions(r_list)
    
create_uplift_tree(df, r_copy2)
