# homework1:  hash_table.py
### 実装した関数
- calculate_hash
- put
- get
- delete  
- resize
- expand_hash
- shrink_hash
- next_prime

### calculate_hash関数について
- 最初のhashの値を0とし、keyに含まれるそれぞれの文字cに対してord(c)で整数に変換する
- その後その時点のhashの値を31でかけord(c)を足し1000000007で割ったものの新しいhashの値として更新し、全ての文字cに対して行う
- 文字の順番を区別し、31,1000000007など素数を用いることにより衝突する確率を減らす

### put関数について
- 
- 

### get関数について
- 
-

### delete関数 について
-
-

### resize関数について
-
-

### expand_hash について
- bucket_sizeとitem_countを比較し
-

### shrink_hash について
- 

### next_prime について
- 

