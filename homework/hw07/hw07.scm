(define (cddr s)
  (cdr (cdr s)))

(define (cadr s)
  (car (cdr s))
)

(define (caddr s)
    (car (cdr (cdr s)))
)

(define (sign x)
  'YOUR-CODE-HERE
  (cond
    ((< x 0) -1)
    ((eq? x 0) 0)
    ((> x 0) 1)
    )
)

(define (square x) (* x x))

(define (pow b n)
  'YOUR-CODE-HERE
  (cond
    ( (eq? n 0) 1 ) ;base case
    ( (even? n) (square (pow b (/ n 2))))
    ( (odd? n) (* b (square (pow b (/ (- n 1) 2)))))
    )
)

(define (ordered? s)
  'YOUR-CODE-HERE
  (cond
        ((or (null? s) (null? (cdr s))) #t) ; base case
        ((or (> (car (cdr s)) (car s)) (eq? (car (cdr s)) (car s))) (ordered? (cdr s)))
        (else #f)
        )
)
