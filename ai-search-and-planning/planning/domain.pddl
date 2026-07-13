(define (domain lunar-rover)
  (:requirements :strips :typing)
  (:types
    rover lander waypoint instrument sample target
  )

  (:predicates
    ;; map / positions
    (adjacent ?a - waypoint ?b - waypoint)   ; undirected edge declared in the problem
    (at ?r - rover ?w - waypoint)            ; rover location
    (at-l ?l - lander ?w - waypoint)         ; lander location (fixed in missions)

    ;; hardware / capabilities
    (on-board ?r - rover ?i - instrument)    ; instrument mounted on rover
    (instrument ?i - instrument)
    (supports-imaging ?i - instrument)
    (supports-sampling ?i - instrument)
    (powered ?i - instrument)                ; keep it simple: instruments already powered

    ;; science targets in the world
    (target-at ?t - target ?w - waypoint)    ; where to take a photo
    (sample-at ?s - sample ?w - waypoint)    ; where to collect a sample

    ;; collected data
    (has-image ?r - rover ?t - target)
    (has-sample ?r - rover ?s - sample)

    ;; transmission state (to the lander / mission control)
    (image-sent ?t - target)
    (sample-sent ?s - sample)
  )

  ;; Move the rover along a traversable edge
  (:action drive
    :parameters (?r - rover ?from - waypoint ?to - waypoint)
    :precondition (and
      (at ?r ?from)
      (adjacent ?from ?to)
    )
    :effect (and
      (at ?r ?to)
      (not (at ?r ?from))
    )
  )

  ;; Take an image of a target at the current waypoint using an imaging instrument
  (:action take-image
    :parameters (?r - rover ?i - instrument ?t - target ?w - waypoint)
    :precondition (and
      (at ?r ?w)
      (on-board ?r ?i)
      (instrument ?i)
      (supports-imaging ?i)
      (powered ?i)
      (target-at ?t ?w)
      (not (has-image ?r ?t))
    )
    :effect (has-image ?r ?t)
  )

  ;; Collect a geological sample at the current waypoint using a sampling instrument
  (:action collect-sample
    :parameters (?r - rover ?i - instrument ?s - sample ?w - waypoint)
    :precondition (and
      (at ?r ?w)
      (on-board ?r ?i)
      (instrument ?i)
      (supports-sampling ?i)
      (powered ?i)
      (sample-at ?s ?w)
      (not (has-sample ?r ?s))
    )
    :effect (has-sample ?r ?s)
  )

  ;; Transmit an image when rover and lander are co-located
  (:action transmit-image
    :parameters (?r - rover ?l - lander ?t - target ?w - waypoint)
    :precondition (and
      (has-image ?r ?t)
      (at ?r ?w)
      (at-l ?l ?w)
      (not (image-sent ?t))
    )
    :effect (image-sent ?t)
  )

  ;; Transmit a sample when rover and lander are co-located
  (:action transmit-sample
    :parameters (?r - rover ?l - lander ?s - sample ?w - waypoint)
    :precondition (and
      (has-sample ?r ?s)
      (at ?r ?w)
      (at-l ?l ?w)
      (not (sample-sent ?s))
    )
    :effect (sample-sent ?s)
  )
)
