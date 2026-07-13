(define (problem mission1)
  (:domain lunar-rover)

  (:objects
    ;; agents
    r1 - rover
    l1 - lander

    ;; waypoints
    w1 w2 w3 w4 - waypoint

    ;; instruments
    cam1 drill1 - instrument

    ;; science targets
    tA - target
    sA - sample
  )

  ;; map: undirected edges -> declare both directions
  (:init
    (adjacent w1 w2) (adjacent w2 w1)
    (adjacent w2 w3) (adjacent w3 w2)
    (adjacent w3 w4) (adjacent w4 w3)
    (adjacent w1 w4) (adjacent w4 w1)

    ;; initial positions
    (at r1 w1)
    (at-l l1 w1)

    ;; instruments mounted and powered
    (instrument cam1) (supports-imaging cam1) (powered cam1) (on-board r1 cam1)
    (instrument drill1) (supports-sampling drill1) (powered drill1) (on-board r1 drill1)

    ;; targets in the world
    (target-at tA w2)   ; take an image at w2
    (sample-at sA w3)   ; collect a sample at w3
  )

  ;; Goal: capture the image and collect+transmit the sample and image
  (:goal (and
    (image-sent tA)
    (sample-sent sA)
  ))
)
