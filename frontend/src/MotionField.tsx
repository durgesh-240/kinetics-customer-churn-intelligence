import { useEffect, useRef } from 'react'

type MotionNode = {
    x: number
    y: number
    vx: number
    vy: number
    radius: number
    phase: number
}

type Signal = {
    from: number
    to: number
    progress: number
    speed: number
}

const NODE_COUNT = 55
const CONNECTION_DISTANCE = 190

/*
 * KINETICS motion palette
 *
 * Warm editorial neutrals instead of cold blue.
 */
const COLORS = {
    line: 'rgba(91, 84, 77, 0.14)',
    lineStrong: 'rgba(91, 84, 77, 0.22)',

    node: 'rgba(91, 84, 77, 0.32)',
    nodeStrong: 'rgba(91, 84, 77, 0.48)',

    glow: 'rgba(132, 121, 109, 0.10)',
    glowSoft: 'rgba(132, 121, 109, 0.045)',

    signal: 'rgba(57, 112, 91, 0.72)',
    signalGlow: 'rgba(57, 112, 91, 0.20)',

    accent: 'rgba(163, 67, 53, 0.48)',
}

export default function MotionField() {
    const canvasRef =
        useRef<HTMLCanvasElement | null>(null)

    useEffect(() => {
        const canvas = canvasRef.current

        if (!canvas) {
            return
        }

        const context = canvas.getContext('2d')

        if (!context) {
            return
        }

        let animationFrame = 0
        let width = 0
        let height = 0
        let dpr = 1

        const mouse = {
            x: 0.5,
            y: 0.5,
            targetX: 0.5,
            targetY: 0.5,
        }

        const nodes: MotionNode[] = []
        const signals: Signal[] = []

        const random = (
            min: number,
            max: number,
        ) =>
            Math.random() *
            (max - min) +
            min

        /*
         * --------------------------------------------------
         * CREATE INTELLIGENCE NODES
         * --------------------------------------------------
         */

        const createNode = (): MotionNode => ({
            x: Math.random(),
            y: Math.random(),

            vx: random(
                -0.00013,
                0.00013,
            ),

            vy: random(
                -0.00010,
                0.00010,
            ),

            radius: random(
                1.3,
                2.8,
            ),

            phase: random(
                0,
                Math.PI * 2,
            ),
        })

        for (
            let index = 0;
            index < NODE_COUNT;
            index += 1
        ) {
            nodes.push(createNode())
        }

        /*
         * --------------------------------------------------
         * CREATE DATA SIGNALS
         * --------------------------------------------------
         */

        for (
            let index = 0;
            index < 14;
            index += 1
        ) {
            signals.push({
                from:
                    Math.floor(
                        Math.random() *
                        NODE_COUNT,
                    ),

                to:
                    Math.floor(
                        Math.random() *
                        NODE_COUNT,
                    ),

                progress:
                    Math.random(),

                speed:
                    random(
                        0.0015,
                        0.0035,
                    ),
            })
        }

        /*
         * --------------------------------------------------
         * RESIZE
         * --------------------------------------------------
         */

        const resize = () => {
            const rect =
                canvas.getBoundingClientRect()

            width = rect.width
            height = rect.height

            dpr =
                Math.min(
                    window.devicePixelRatio ||
                    1,
                    2,
                )

            canvas.width =
                Math.floor(
                    width * dpr,
                )

            canvas.height =
                Math.floor(
                    height * dpr,
                )

            context.setTransform(
                dpr,
                0,
                0,
                dpr,
                0,
                0,
            )
        }

        /*
         * --------------------------------------------------
         * POINTER INTERACTION
         * --------------------------------------------------
         */

        const handlePointerMove = (
            event: PointerEvent,
        ) => {
            mouse.targetX =
                event.clientX /
                window.innerWidth

            mouse.targetY =
                event.clientY /
                window.innerHeight
        }

        const handlePointerLeave = () => {
            mouse.targetX = 0.5
            mouse.targetY = 0.5
        }

        /*
         * --------------------------------------------------
         * DISTANCE
         * --------------------------------------------------
         */

        const distance = (
            a: MotionNode,
            b: MotionNode,
        ) => {
            const dx =
                (a.x - b.x) *
                width

            const dy =
                (a.y - b.y) *
                height

            return Math.sqrt(
                dx * dx +
                dy * dy,
            )
        }

        /*
         * --------------------------------------------------
         * MAIN ANIMATION
         * --------------------------------------------------
         */

        const draw = (
            time: number,
        ) => {
            context.clearRect(
                0,
                0,
                width,
                height,
            )

            /*
             * Smooth pointer movement.
             */
            mouse.x +=
                (mouse.targetX -
                    mouse.x) *
                0.035

            mouse.y +=
                (mouse.targetY -
                    mouse.y) *
                0.035

            /*
             * Very subtle parallax.
             */
            const mouseOffsetX =
                (mouse.x - 0.5) *
                24

            const mouseOffsetY =
                (mouse.y - 0.5) *
                18

            /*
             * ------------------------------------------------
             * MOVE NODES
             * ------------------------------------------------
             */

            nodes.forEach(
                (node) => {
                    node.x += node.vx
                    node.y += node.vy

                    if (
                        node.x < -0.05 ||
                        node.x > 1.05
                    ) {
                        node.vx *= -1
                    }

                    if (
                        node.y < -0.05 ||
                        node.y > 1.05
                    ) {
                        node.vy *= -1
                    }
                },
            )

            /*
             * ------------------------------------------------
             * NETWORK LINES
             * ------------------------------------------------
             */

            for (
                let i = 0;
                i < nodes.length;
                i += 1
            ) {
                for (
                    let j = i + 1;
                    j < nodes.length;
                    j += 1
                ) {
                    const first =
                        nodes[i]

                    const second =
                        nodes[j]

                    const distanceBetween =
                        distance(
                            first,
                            second,
                        )

                    if (
                        distanceBetween >
                        CONNECTION_DISTANCE
                    ) {
                        continue
                    }

                    const strength =
                        1 -
                        distanceBetween /
                        CONNECTION_DISTANCE

                    const firstX =
                        first.x *
                        width +
                        mouseOffsetX

                    const firstY =
                        first.y *
                        height +
                        mouseOffsetY

                    const secondX =
                        second.x *
                        width +
                        mouseOffsetX

                    const secondY =
                        second.y *
                        height +
                        mouseOffsetY

                    context.beginPath()

                    context.moveTo(
                        firstX,
                        firstY,
                    )

                    context.lineTo(
                        secondX,
                        secondY,
                    )

                    /*
                     * Warm graphite lines.
                     */
                    context.strokeStyle =
                        strength > 0.55
                            ? COLORS.lineStrong
                            : COLORS.line

                    context.lineWidth =
                        0.65 +
                        strength * 0.55

                    context.stroke()
                }
            }

            /*
             * ------------------------------------------------
             * NODES
             * ------------------------------------------------
             */

            nodes.forEach(
                (node) => {
                    const pulse =
                        Math.sin(
                            time *
                            0.0012 +
                            node.phase,
                        ) *
                        0.25 +
                        0.75

                    const x =
                        node.x *
                        width +
                        mouseOffsetX

                    const y =
                        node.y *
                        height +
                        mouseOffsetY

                    /*
                     * Soft warm halo.
                     */
                    const glow =
                        context.createRadialGradient(
                            x,
                            y,
                            0,
                            x,
                            y,
                            node.radius *
                            7,
                        )

                    glow.addColorStop(
                        0,
                        COLORS.glow,
                    )

                    glow.addColorStop(
                        0.45,
                        COLORS.glowSoft,
                    )

                    glow.addColorStop(
                        1,
                        'rgba(132, 121, 109, 0)',
                    )

                    context.fillStyle =
                        glow

                    context.beginPath()

                    context.arc(
                        x,
                        y,
                        node.radius * 7,
                        0,
                        Math.PI * 2,
                    )

                    context.fill()

                    /*
                     * Main node.
                     */
                    context.beginPath()

                    context.arc(
                        x,
                        y,
                        node.radius *
                        pulse,
                        0,
                        Math.PI * 2,
                    )

                    context.fillStyle =
                        pulse > 0.88
                            ? COLORS.nodeStrong
                            : COLORS.node

                    context.fill()
                },
            )

            /*
             * ------------------------------------------------
             * MOVING DATA SIGNALS
             * ------------------------------------------------
             */

            signals.forEach(
                (signal) => {
                    const from =
                        nodes[
                            signal.from
                            ]

                    const to =
                        nodes[
                            signal.to
                            ]

                    if (
                        !from ||
                        !to
                    ) {
                        return
                    }

                    signal.progress +=
                        signal.speed

                    /*
                     * Pick a new route.
                     */
                    if (
                        signal.progress >=
                        1
                    ) {
                        signal.progress = 0

                        signal.from =
                            Math.floor(
                                Math.random() *
                                NODE_COUNT,
                            )

                        signal.to =
                            Math.floor(
                                Math.random() *
                                NODE_COUNT,
                            )
                    }

                    const x =
                        (
                            from.x +
                            (to.x -
                                from.x) *
                            signal.progress
                        ) *
                        width +
                        mouseOffsetX

                    const y =
                        (
                            from.y +
                            (to.y -
                                from.y) *
                            signal.progress
                        ) *
                        height +
                        mouseOffsetY

                    /*
                     * Signal halo.
                     */
                    const signalGlow =
                        context.createRadialGradient(
                            x,
                            y,
                            0,
                            x,
                            y,
                            16,
                        )

                    signalGlow.addColorStop(
                        0,
                        COLORS.signalGlow,
                    )

                    signalGlow.addColorStop(
                        1,
                        'rgba(57, 112, 91, 0)',
                    )

                    context.fillStyle =
                        signalGlow

                    context.beginPath()

                    context.arc(
                        x,
                        y,
                        16,
                        0,
                        Math.PI * 2,
                    )

                    context.fill()

                    /*
                     * Signal core.
                     */
                    context.beginPath()

                    context.arc(
                        x,
                        y,
                        2.5,
                        0,
                        Math.PI * 2,
                    )

                    context.fillStyle =
                        COLORS.signal

                    context.shadowBlur =
                        10

                    context.shadowColor =
                        COLORS.signalGlow

                    context.fill()

                    context.shadowBlur = 0
                },
            )

            /*
             * ------------------------------------------------
             * VERY SUBTLE AMBIENT LIGHT
             * ------------------------------------------------
             */

            const glowX =
                width *
                (
                    0.5 +
                    Math.sin(
                        time *
                        0.00012,
                    ) *
                    0.30
                )

            const glowY =
                height *
                (
                    0.5 +
                    Math.cos(
                        time *
                        0.00016,
                    ) *
                    0.25
                )

            const gradient =
                context.createRadialGradient(
                    glowX,
                    glowY,
                    0,
                    glowX,
                    glowY,
                    Math.min(
                        width,
                        height,
                    ) * 0.48,
                )

            gradient.addColorStop(
                0,
                'rgba(132, 121, 109, 0.035)',
            )

            gradient.addColorStop(
                0.45,
                'rgba(132, 121, 109, 0.018)',
            )

            gradient.addColorStop(
                1,
                'rgba(132, 121, 109, 0)',
            )

            context.fillStyle =
                gradient

            context.fillRect(
                0,
                0,
                width,
                height,
            )

            animationFrame =
                requestAnimationFrame(
                    draw,
                )
        }

        resize()

        window.addEventListener(
            'resize',
            resize,
        )

        window.addEventListener(
            'pointermove',
            handlePointerMove,
            {
                passive: true,
            },
        )

        window.addEventListener(
            'pointerleave',
            handlePointerLeave,
        )

        animationFrame =
            requestAnimationFrame(
                draw,
            )

        return () => {
            cancelAnimationFrame(
                animationFrame,
            )

            window.removeEventListener(
                'resize',
                resize,
            )

            window.removeEventListener(
                'pointermove',
                handlePointerMove,
            )

            window.removeEventListener(
                'pointerleave',
                handlePointerLeave,
            )
        }
    }, [])

    return (
        <canvas
            ref={canvasRef}
            className="motion-field"
            aria-hidden="true"
        />
    )
}