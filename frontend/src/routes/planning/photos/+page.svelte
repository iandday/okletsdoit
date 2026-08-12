<script lang="ts">
    import { enhance } from "$app/forms";
    import { goto } from "$app/navigation";
    import { invalidateAll } from "$app/navigation";
    import PhotoGallery from "$lib/components/PhotoGallery.svelte";
    import ProtectedPageHeader from "$lib/components/layouts/ProtectedPageHeader.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";
    import "photoswipe/dist/photoswipe.css";
    import { onMount } from "svelte";
    import type { PageData, ActionData } from "./$types";

    const { data }: { data: PageData } = $props();
    const relativeCrumbs = [{ title: "Photo Review" }];
    let socket: WebSocket | undefined;
    let reconnectTimer: ReturnType<typeof setTimeout> | undefined;
    let reconnectAttempts = 0;
    let shouldReconnect = true;

    const connectPhotoUpdates = () => {
        const protocol = window.location.protocol === "https:" ? "wss" : "ws";
        const wsUrl = `${protocol}://${window.location.host}/ws/photos/`;

        socket = new WebSocket(wsUrl);

        socket.onopen = () => {
            reconnectAttempts = 0;
        };

        socket.onmessage = async (event: MessageEvent<string>) => {
            try {
                const payload = JSON.parse(event.data) as { event?: string };
                if (payload.event === "photo.ready" || payload.event === "photo.failed") {
                    await invalidateAll();
                }
            } catch {
                // Ignore malformed websocket payloads.
            }
        };

        socket.onclose = () => {
            if (!shouldReconnect) return;
            reconnectAttempts += 1;
            const delay = Math.min(10000, 1000 * reconnectAttempts);
            reconnectTimer = setTimeout(connectPhotoUpdates, delay);
        };

        socket.onerror = () => {
            socket?.close();
        };
    };

    onMount(() => {
        let lightbox: any;

        const setupLightbox = async () => {
            const { default: PhotoSwipeLightbox } = await import("photoswipe/lightbox");
            lightbox = new PhotoSwipeLightbox({
                gallery: "#photoswipe-gallery",
                children: "a",
                pswpModule: () => import("photoswipe"),
                bgOpacity: 0.9,
            });

            lightbox.on("uiRegister", () => {
                if (!lightbox) return;

                lightbox.pswp.ui.registerElement({
                    name: "download-button",
                    order: 8,
                    isButton: true,
                    className: "pswp__button pswp__button--download",
                    title: "Download image",
                    html: {
                        isCustomSVG: true,
                        inner: '<path d="M9.5 4.5h5v7.8l2.4-2.4 1.4 1.4-4.8 4.8-4.8-4.8 1.4-1.4 2.4 2.4z"/><path d="M5 18.5h14v2H5z"/>',
                        outlineID: "pswp__icn-download",
                        size: 24,
                    },
                    onClick: (_event: MouseEvent, _el: HTMLElement, pswp: any) => {
                        const photoId = pswp.currSlide?.data?.element?.dataset?.photoId as string | undefined;
                        if (!photoId) return;

                        window.location.assign(`/api/photos/uploaded/${photoId}/download`);
                    },
                });

                lightbox.pswp.ui.registerElement({
                    name: "counter-indicator",
                    order: 9,
                    isButton: false,
                    appendTo: "bar",
                    className: "pswp__custom-counter",
                    html: "1 / 1",
                    onInit: (el: HTMLElement, pswp: any) => {
                        const updateCounter = () => {
                            el.textContent = `${pswp.currIndex + 1} / ${pswp.getNumItems()}`;
                        };

                        pswp.on("change", updateCounter);
                        pswp.on("afterInit", updateCounter);
                    },
                });
            });

            lightbox.init();
        };

        setupLightbox();
        connectPhotoUpdates();

        return () => {
            shouldReconnect = false;
            if (reconnectTimer) {
                clearTimeout(reconnectTimer);
            }
            socket?.close();
            lightbox?.destroy();
        };
    });
</script>

<ProtectedPageShell {relativeCrumbs}>
    <ProtectedPageHeader title="Photo Review" description="Review and manage uploaded photos" />
    <PhotoGallery photos={data.photos} />
</ProtectedPageShell>
