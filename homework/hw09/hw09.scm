;;; Homework 09: Scheme List, Tail Recursion and Macro

;;; Required Problems

(define (make-change total biggest)
        (if (> biggest total)
            (define biggest total)
        )
        (if (<= biggest 0)
            (list)
            (if (= total biggest)
                (append (list (list total)) (make-change total (- biggest 1)))
                (append (map (lambda (lst1) (cons biggest lst1))
                             (make-change (- total biggest) biggest))
                        (make-change total (- biggest 1)))
            )
        )
)


(define (find n lst)
        (define (find_with_count n lst i)
                (if (= (car lst) n)
                    i
                    (find_with_count n (cdr lst) (+ i 1))
                )
        )
        (find_with_count n lst 0)
)


(define (find-nest n sym)
        (define (exist n sym)
                (if (null? sym)
                    #f
                    (if (null? (cdr sym))
                        (if (pair? (car sym))
                            (exist n (car sym))
                            (if (eq? (car sym) n)
                                #t
                                #f
                            )
                        )
                        (if (pair? (car sym))
                            (or (exist n (car sym)) (exist n (cdr sym)))
                            (if (eq? (car sym) n)
                                #t
                                (exist n (cdr sym))
                            )
                        )
                    )
                )
          )
          (define (with_lst n lsting sym)
                  (if (pair? (car lsting))
                      (if (exist n (car lsting))
                          (list 'car (with_lst n (car lsting) sym))
                          (list 'cdr (with_lst n (cdr lsting) sym))
                      )
                      (if (eq? (car lsting) n)
                          (list 'car sym)
                          (list 'cdr (with_lst n (cdr lsting) sym))
                      )
                  )
          )
          (define (reverse lst sym)
                  (if (pair? (car (cdr lst)))
                      (reverse (car (cdr lst)) `(,(car lst) ,sym))
                      `(,(car lst) ,sym)
                  )
          )
          (reverse (with_lst n (eval sym) sym) sym)
)


(define-macro (my/or operands)
              (cond 
              ((null? operands) #f)
              ((null? (cdr operands)) (car operands))
              (else
             `(let ((t ,(car operands)))
                    (if (not t)
                        (my/or ,(cdr operands))
                        t)
              )
              )
                    )
)

(define (get-nth-ele lst n)
    (if (= n 0)
        (car lst)
        (get-nth-ele (cdr lst) (- n 1))
    )
)

(define (replaced-para args indices)
    (if (null? indices)
        (list)
        (cons (get-nth-ele args (car indices)) (replaced-para args (cdr indices)))
    )
)

(define (in ele lst)
    (if (null? lst)
        #f
        (if (eq? ele (car lst))
            #t
            (in ele (cdr lst))
        )
    )
)

(define (not-replaced-para args indices)
    (define replaced-one (replaced-para args indices))
    (filter (lambda (x) (not (in x replaced-one))) args)
)
(define (zip lst1 lst2)
    (if (null? lst1)
        (list)
        (cons (list (car lst1) (car lst2)) (zip (cdr lst1) (cdr lst2)))
    )
)
(define-macro (k-curry fn args vals indices)
    `(lambda
        ,(not-replaced-para args indices)
        (let ,(zip (replaced-para args indices) vals)
            (,fn ,@args)
        )
    )
)

(define-macro (let* bindings expr)
              (if (null? bindings)
                 `(let () ,expr)
                 `(let  (,(car bindings))
                        (let* ,(cdr bindings) ,expr)
                  )
              )
)

;;; Just For Fun Problems


; Helper Functions for you
(define (cadr lst) (car (cdr lst)))
(define (cddr lst) (cdr (cdr lst)))
(define (caddr lst) (car (cdr (cdr lst))))
(define (cdddr lst) (cdr (cdr (cdr lst))))

(define-macro (infix expr)
  'YOUR-CODE-HERE
)


; only testing if your code could expand to a valid expression 
; resulting in my/and/2 and my/or/2 not hygienic
(define (gen-sym) 'sdaf-123jasf/a123)

; in these two functions you can use gen-sym function.
; assumption:
; 1. scm> (eq? (gen-sym) (gen-sym))
;    #f
; 2. all symbol generate by (gen-sym) will not in the source code before macro expansion
(define-macro (my/and/2 operands)
  'YOUR-CODE-HERE
)

(define-macro (my/or/2 operands)
  'YOUR-CODE-HERE
)