(define (accumulate combiner start n term)
  (if (= n 0) start
    (combiner (accumulate combiner start (- n 1) term) (term n))
    )
)

(define (accumulate-tail combiner start n term)
  (define (help-accumulate combiner start n term curr-result)
    (if (= n 0) curr-result
        (begin
            (define so-far (combiner curr-result (term n)))
            (help-accumulate combiner start (- n 1) term so-far)
            )
        ) ; close if

    ) ; close inner define
    (help-accumulate combiner start n term start)
) ; close outer define

(define (rle s)
  (define (help-count s count num-sofar)

    (if (null? s)
            (cons-stream (list num-sofar count) nil)
            (if (= num-sofar (car s))

                (help-count (cdr-stream s) (+ count 1) num-sofar)
                (cons-stream (list num-sofar count) (help-count (cdr-stream s) 1 (car s)))

                ) ; close if

            ) ; close outer if
    )
(if (null? s)
    nil
(help-count (cdr-stream s) 1 (car s))
)
)

;    (if (or (null? s) (null? (cdr-stream s)))
;        (cons-stream (car s) (cons-stream count nil)) ; if end of the stream, list the number and count


;    (if (= (car (cdr-stream s)) (car s))
;        (help-count (cdr-stream s) (+ 1 count)) ; if same element, add one to count
;        (help-count (cdr-stream s) 1) ; if element not the same, change the start and restart

;        ) ; close if
;    )


;    ); close inner define

;(help-count s 1)
;) ; close outer define
