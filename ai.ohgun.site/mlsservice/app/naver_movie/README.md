# Naver sentiment movie corpus v1.0

This is a movie review dataset in the Korean language.
Reviews were scraped from [Naver Movies](http://movie.naver.com/movie/point/af/list.nhn).

The dataset construction is based on the method noted in [Large movie review dataset](http://ai.stanford.edu/~amaas/data/sentiment/) from Maas et al., 2011.


## Data description

- Each file is consisted of three columns: `id`, `document`, `label`
    - `id`: The review id, provieded by Naver
    - `document`: The actual review
    - `label`: The sentiment class of the review. (0: negative, 1: positive)
    - Columns are delimited with tabs (i.e., `.tsv` format; but the file extension is `.txt` for easy access for novices)
- 200K reviews in total
    - `ratings.txt`: All 200K reviews
    - `ratings_test.txt`: 50K reviews held out for testing
    - `ratings_train.txt`: 150K reviews for training

## Characteristics

- All reviews are shorter than 140 characters
- Each sentiment class is sampled equally (i.e., random guess yields 50% accuracy)
    - 100K negative reviews (originally reviews of ratings 1-4)
    - 100K positive reviews (originally reviews of ratings 9-10)
    - Neutral reviews (originally reviews of ratings 5-8) are excluded

## Quick peek

    $ head ratings_train.txt
    id      document        label
    9976970 ???”ë¹™.. ì§„ì§œ ì§œì¦?˜ë„¤??ëª©ì†Œë¦?       0
    3819312 ??..?¬ìŠ¤?°ë³´ê³?ì´ˆë”©?í™”ì¤?...?¤ë²„?°ê¸°ì¡°ì°¨ ê°€ë³ì? ?Šêµ¬??       1
    10265843        ?ˆë¬´?¬ë°“?ˆë‹¤ê·¸ë˜?œë³´?”ê²ƒ?„ì¶”ì²œí•œ??     0
    9045019 êµë„???´ì•¼ê¸°êµ¬ë¨?..?”ì§???¬ë????†ë‹¤..?‰ì  ì¡°ì •       0
    6483659 ?¬ì´ëª¬í˜ê·¸ì˜ ?µì‚´?¤ëŸ° ?°ê¸°ê°€ ?‹ë³´?€???í™”!?¤íŒŒ?´ë”ë§¨ì—???™ì–´ë³´ì´ê¸°ë§Œ ?ˆë˜ ì»¤ìŠ¤???˜ìŠ¤?¸ê? ?ˆë¬´?˜ë„ ?´ë»ë³´ì??? 1
    5403919 ë§?ê±¸ìŒë§??€ 3?¸ë???ì´ˆë“±?™êµ 1?™ë…„?ì¸ 8?´ìš©?í™”.?‹ã…‹??..ë³„ë°˜ê°œë„ ?„ê¹Œ?€.     0
    7797314 ?ì‘??ê¸´ì¥ê°ì„ ?œë?ë¡??´ë ¤?´ì?ëª»í–ˆ??  0
    9443947 ë³?ë°˜ê°œ???„ê¹???•ë‚˜?¨ë‹¤ ?´ì‘ê²?ê¸¸ìš©???°ê¸°?í™œ?´ëª‡?„ì¸ì§€..?•ë§ ë°œë¡œ?´ë„ ê·¸ê²ƒë³´ë‹¨ ?«ê²Ÿ???©ì¹˜.ê°ê¸ˆë§Œë°˜ë³µë°˜ë³?.?´ë“œ?¼ë§ˆ??ê°€ì¡±ë„?†ë‹¤ ?°ê¸°ëª»í•˜?”ì‚¬?Œë§Œëª¨ì—¿??      0
    7156791 ?¡ì…˜???†ëŠ”?°ë„ ?¬ë? ?ˆëŠ” ëª‡ì•ˆ?˜ëŠ” ?í™” 1

## License

<p xmlns:dct="http://purl.org/dc/terms/">
  <a rel="license"
     href="http://creativecommons.org/publicdomain/zero/1.0/">
    <img src="http://i.creativecommons.org/p/zero/1.0/88x31.png" style="border-style: none;" alt="CC0" />
  </a>
</p>
