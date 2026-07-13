(define (problem mission2)
  (:domain lunar-rover)

  (:objects
    ;; agents
    r1 r2 - rover
    l1 l2 - lander

    ;; waypoints (denser map)
    w1 w2 w3 w4 w5 - waypoint

    ;; instruments
    cam1 cam2 - instrument
    drill1 drill2 - instrument

    ;; science targets / samples
    tA tB - target
    sA sB - sample
  )

  (:init
    ;; map: make a small network
    (adjacent w1 w2) (adjacent w2 w1)
    (adjacent w2 w3) (adjacent w3 w2)
    (adjacent w3 w4) (adjacent w4 w3)
    (adjacent w4 w5) (adjacent w5 w4)
    (adjacent w1 w5) (adjacent w5 w1)
    (adjacent w2 w5) (adjacent w5 w2)

    ;; positions
    (at r1 w1)
    (at r2 w4)
    (at-l l1 w1)
    (at-l l2 w4)

    ;; instruments on rovers (each rover has camera + drill)
    (instrument cam1) (supports-imaging cam1) (powered cam1) (on-board r1 cam1)
    (instrument drill1) (supports-sampling drill1) (powered drill1) (on-board r1 drill1)
    (instrument cam2) (supports-imaging cam2) (powered cam2) (on-board r2 cam2)
    (instrument drill2) (supports-sampling drill2) (powered drill2) (on-board r2 drill2)

    ;; targets/samples in world
    (target-at tA w2)
    (target-at tB w5)
    (sample-at sA w3)
    (sample-at sB w5)
  )

  ;; Goals: collect & transmit two images and two samples (can be shared across rovers/landers)
  (:goal (and
    (image-sent tA)
    (image-sent tB)
    (sample-sent sA)
    (sample-sent sB)
  ))
)
