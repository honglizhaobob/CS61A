; Lab 13: Final Review

(define (compose-all funcs)
  (if (null? funcs)
    (lambda (x) x)
    (begin
        (define curr-func (car funcs))
        (lambda (x) ((compose-all (cdr funcs)) (curr-func x)))
        )
    )
)

