# 2024-Spring-HW2

Please complete the report problem below:

## Problem 1
Provide your profitable path, the amountIn, amountOut value for each swap, and your final reward (your tokenB balance).

path: tokenB->tokenA->tokenC->tokenE->tokenD->tokenC->tokenB

|  | amountIn | amountOut |
| -------- | -------- | -------- |
| tokenB->tokenA     |   5    |   5.655321988655322  |
| tokenA->tokenC     |   5.655321988655322   |   2.372138936383089   |
| tokenC->tokenE     |    2.372138936383089  |   1.5301371369636168   |
| tokenE->tokenD     |    1.5301371369636168  |   3.450741448619708   |
| tokenD->tokenC     |    3.450741448619708  |   6.684525579572586   |
| tokenC->tokenB     |    6.684525579572586  |   22.49722180697414   |


final reward: tokenB balance=22.49722180697414

## Problem 2
What is slippage in AMM, and how does Uniswap V2 address this issue? Please illustrate with a function as an example.

slippage指的是我們交易時的預期價格和實際執行價格之間的差異.產生slippage的原因可能是因為當你得到報價時會有一段時間讓你可以決定要不要接受,而如果有人在這段時間內在同個pool進行swap,那麼pool中的token數量會和你想要交易時有所不同,因此假如最後你接受報價進行swap,那麼你得到的token數量便會和你預期的不同,我們就稱之為slippage
假如目前pool中tokenA : tokenB = 1 : 10.(先假設不會有fee)
假如你想要用10個B來交換A,那麼此時的報價會是你能得到0.5個A(由於x\*y=k,所以1\*10 = 0.5\*20),在你接受swap前,突然有人用2.5個B先swap了0.2個A(0.8\*12.5=10),那麼你接受交易後,就會變成用10個B swap 0.35556個A(0.444444\*22.5=10),因此產生了slippage(預期換到0.5個A最後只換到0.35556個A)

## Problem 3
Please examine the mint function in the UniswapV2Pair contract. Upon initial liquidity minting, a minimum liquidity is subtracted. What is the rationale behind this design?


之所以要先減掉minimum liquidity是為了防止有攻擊者去惡意提高提供流動性的門檻(inflation attack).
假如不需要減掉minimum liquidity,那麼攻擊者能夠先transfer很小數量的token(比如1 wei)到pair,得到1 wei LP Tokens,此時pool中totalsupply=1 wei,reverse0和reverse1也是1 wei.
之後攻擊者能夠transfer大量token(比如說2000 ether)到pair,但不call mint()而是call sync(),此時total supply還會是1 wei,但reverse0和reverse1會變成1 wei + 2000 ether.
那麼這時這個pair的價格會變成(1+2000\*10^18)/1,約為2000 ether,代表其他人就算只是想要提供1 wei流動性都需要付出2000 ether的token.代表流動性被攻擊者壟斷
(順帶一題,此時uniswap也幾乎收不到手續費)
為了解決這個問題,當首次mint pair時,改成需要減去minimum liquidity,這樣一來,就代表pool中的totalsupply至少是minimum liquidity+1,因此當攻擊者想要用同樣手法攻擊時,pair的價格會是(1001+2000\*10^18)/1001,約為2 ether,因此其他人便不用付出2000 ether才能增加流動性
(uniswap也能收到手續費)

## Problem 4
Investigate the minting function in the UniswapV2Pair contract. When depositing tokens (not for the first time), liquidity can only be obtained using a specific formula. What is the intention behind this?


之所以要用liquidity = Math.min(amount0.mul(_totalSupply) \/ _reserve0, amount1.mul(_totalSupply) / _reserve1);
這個formula來決定用戶所供的liquidity是因為,假如目前有1個pair有10個tokenA和10個tokenB,那麼假如user提供10個tokenA和0個tokenB,那麼它應該要得到0/10的liquidity.又比如說一個user提供價值目前5%的tokenA和10%的tokenB,那麼它應該要得到價值5%的tokenA.這是因為我們不希望用戶提供的token數量影響到pair的token ratio,也就是說我們希望pair(假如x個tokenA和y個tokenB)加上user提供的token後依舊能維持(x+x')*(y+y')=k.

## Problem 5
What is a sandwich attack, and how might it impact you when initiating a swap?

sandwich attack是一種MEV攻擊,指的是攻擊者會先持續監控 Mempool，當其在 Mempool 中發現有受害者想要進行一筆交易時，攻擊者可以先在受害者的交易前面放置另一個交易讓代幣的價格推到受害者交易能夠承受的最大滑點，之後受害者只能用最大滑點價格進行交易，促使價格進一步推動，最後攻擊者就能用受害者交易完後的價格(相較之下更好的價格)來賣出該代幣以獲取利潤。
因為攻擊者會將交易安插在受害者之前,所以受害者只能用最大滑點價格進行交易,使他受到的slippage最大,而承受了損失.