;;; Lab 10: Stream

;;; Required Problems

(define (filter-stream f s)
  (if (null? s)
    nil
    (if (f (car s))
        (cons-stream (car s) (filter-stream f (cdr-stream s)))
        (filter-stream f (cdr-stream s))
    )
  )
)


(define (slice s start end)
  (cond 
    ((null? s) nil)
    ((> start 0) (slice (cdr-stream s) (- start 1) (- end 1)))
    ((= end 0) nil)
    (else (cons (car s) (slice (cdr-stream s) start (- end 1))))
  )
)


(define (naturals n)
  (cons-stream n (naturals (+ n 1))))


(define (combine-with f xs ys)
  (if (or (null? xs) (null? ys))
      nil
      (cons-stream
        (f (car xs) (car ys))
        (combine-with f (cdr-stream xs) (cdr-stream ys)))))


(define factorials
  (cons-stream 1 (combine-with (lambda (x y) (* x y)) factorials (naturals 1)))
)


(define fibs
  (cons-stream 0 (cons-stream 1 (combine-with (lambda (x y) (+ x y)) fibs (cdr-stream fibs))))
)


(define (exp x)
  (cons-stream 1 (combine-with (lambda (a b) (+ a b)) (combine-with (lambda (a b) (/ (expt x a) b)) (naturals 1) (cdr-stream factorials)) (exp x)))
)


(define (list-to-stream lst)
  (if (null? lst) nil
      (cons-stream (car lst) (list-to-stream (cdr lst)))))


(define (nondecrease s)
  (define (cons-increase s)
    (cond
      ((null? s) (list))
      ((null? (cdr-stream s)) (list (car s)))
      ((< (car (cdr-stream s)) (car s)) (list (car s)))
      (else (append (list (car s)) (cons-increase (cdr-stream s))))
    )
  )
  (define list-now (cons-increase s))
  (define (cdr-n-times n lst)
    (if (= n 0)
        lst
        (cdr-n-times (- n 1) (cdr-stream lst))
    )
  )
  (define length-of-lst (length list-now))
  (if (= length-of-lst 0)
    list-now
    (cons-stream
      list-now
      (nondecrease (cdr-n-times (length list-now) s))
    )
  )
)




;;; Just For Fun Problems

(define (my-cons-stream first second) ; Does this line need to be changed?
  'YOUR-CODE-HERE
)

(define (my-car stream)
  'YOUR-CODE-HERE
)

(define (my-cdr-stream stream)
  'YOUR-CODE-HERE
)


(define (sieve s)
  'YOUR-CODE-HERE
)

(define primes (sieve (naturals 2)))
