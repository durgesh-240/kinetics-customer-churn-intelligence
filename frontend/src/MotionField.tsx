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

/*
 * KINETICS motion palette
 *
 * Warm editorial neutrals instead of cold blue.
 *
 * The mobile version intentionally uses lower opacity
 * so the network remains atmospheric instead of becoming
 * visually dense behind the content.
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

/*
 * ----------------------------------------------------------
 * RESPONSIVE MOTION CONFIGURATION
 * ----------------------------------------------------------
 *
 * Desktop:
 *   Dense enough to communicate intelligence/network activity.
 *
 * Tablet:
 *   Reduced density.
 *
 * Mobile:
 *   Sparse network so the content remains readable.
 *
 * Small phones:
 *   Very restrained network to avoid line clutter.
 */
const getMotionConfig = () => {
    const width = window.innerWidth

    if (width <= 420) {
        return {
            nodeCount: 10,
            connectionDistance: 90,
            signalCount: 2,
            radiusMin: 0.8,
            radiusMax: 1.5,
            lineOpacity: 0.32,
            signalOpacity: 0.45,
            parallaxX: 5,
            parallaxY: 4,
        }
    }

    if (width <= 720) {
        return {
            nodeCount: 14,
            connectionDistance: 105,
            signalCount: 3,
            radiusMin: 0.9,
            radiusMax: 1.7,
            lineOpacity: 0.40,
            signalOpacity: 0.50,
            parallaxX: 7,
            parallaxY: 5,
        }
    }

    if (width <= 1100) {
        return {
            nodeCount: 30,
            connectionDistance: 145,
            signalCount: 7,
            radiusMin: 1.1,
            radiusMax: 2.2,
            lineOpacity: 0.70,
            signalOpacity: 0.75,
            parallaxX: 14,
            parallaxY: 10,
        }
    }

    return {
        nodeCount: 55,
        connectionDistance: 190,
        signalCount: 14,
        radiusMin: 1.3,
        radiusMax: 2.8,
        lineOpacity: 1,
        signalOpacity: 1,
        parallaxX: 24,
        parallaxY: 18,
    }
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

        let config = getMotionConfig()

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
                config.radiusMin,
                config.radiusMax,
            ),

            phase: random(
                0,
                Math.PI * 2,
            ),
        })

        const createSignal = (): Signal => ({
            from:
                Math.floor(
                    Math.random() *
                    config.nodeCount,
                ),

            to:
                Math.floor(
                    Math.random() *
                    config.nodeCount,
                ),

            progress:
                Math.random(),

            speed:
                random(
                    0.0015,
                    0.0035,
                ),
        })

        const rebuildDensity = () => {
            config = getMotionConfig()

            /*
             * Add or remove nodes according to
             * the current viewport density.
             */
            while (
                nodes.length <
                config.nodeCount
                ) {
                nodes.push(createNode())
            }

            if (
                nodes.length >
                config.nodeCount
            ) {
                nodes.splice(
                    config.nodeCount,
                )
            }

            /*
             * Rebuild signal count as well.
             */
            while (
                signals.length <
                config.signalCount
                ) {
                signals.push(
                    createSignal(),
                )
            }

            if (
                signals.length >
                config.signalCount
            ) {
                signals.splice(
                    config.signalCount,
                )
            }

            /*
             * Make sure every signal references
             * a valid node after a density change.
             */
            signals.forEach(
                (signal) => {
                    signal.from =
                        Math.floor(
                            Math.random() *
                            config.nodeCount,
                        )

                    signal.to =
                        Math.floor(
                            Math.random() *
                            config.nodeCount,
                        )
                },
            )
        }

        rebuildDensity()

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

            /*
             * Recalculate motion density when the
             * viewport crosses a responsive breakpoint.
             */
            const previousNodeCount =
                config.nodeCount

            const previousSignalCount =
                config.signalCount

            const nextConfig =
                getMotionConfig()

            if (
                previousNodeCount !==
                nextConfig.nodeCount ||
                previousSignalCount !==
                nextConfig.signalCount
            ) {
                rebuildDensity()
            }
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
             *
             * The effect becomes much smaller on
             * mobile so the network does not feel
             * like it is moving excessively behind
             * the text.
             */
            const mouseOffsetX =
                (mouse.x - 0.5) *
                config.parallaxX

            const mouseOffsetY =
                (mouse.y - 0.5) *
                config.parallaxY

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
                        config.connectionDistance
                    ) {
                        continue
                    }

                    const strength =
                        1 -
                        distanceBetween /
                        config.connectionDistance

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
                     *
                     * Mobile gets an additional opacity
                     * reduction to prevent the network
                     * from becoming visually heavy.
                     */
                    context.globalAlpha =
                        config.lineOpacity

                    context.strokeStyle =
                        strength > 0.55
                            ? COLORS.lineStrong
                            : COLORS.line

                    context.lineWidth =
                        0.65 +
                        strength * 0.55

                    context.stroke()

                    context.globalAlpha = 1
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
                            node.radius * 7,
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

                    context.globalAlpha =
                        config.lineOpacity

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

                    context.globalAlpha = 1
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
                                config.nodeCount,
                            )

                        signal.to =
                            Math.floor(
                                Math.random() *
                                config.nodeCount,
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

                    context.globalAlpha =
                        config.signalOpacity

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

                    context.globalAlpha = 1
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