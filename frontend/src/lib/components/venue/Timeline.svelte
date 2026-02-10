<script lang="ts">
    import type { TimelineSchema } from "../../../../api-client";

    interface venueProps {
        timelineEntries: TimelineSchema[];
    }
    let { timelineEntries = [] }: venueProps = $props();
</script>

<div class="card bg-base-300 shadow-lg p-8">
    <div class="card-body p-0 text-secondary-content">
        <h2
            class="card-body-title text-accent text-2xl mb-2 font-bold text-center gap-4 flex items-center justify-center">
            <span class="icon-[lucide--clock] size-6"></span>Schedule
        </h2>
        <div class="grid grid-cols-1 py-6 justify-items-center gap-4">
            {#if timelineEntries.length === 0}
                <h3 class="text-3xl font-bold text-center">Coming Soon!</h3>
                <p class="text-center">Good things come to those who wait. Stay tuned for our event timeline.</p>
            {:else}
                <div class="w-full max-w-3xl">
                    <ul class="timeline timeline-vertical">
                        {#each timelineEntries as entry, index (entry.order)}
                            <li>
                                <hr class="bg-accent" />
                                <div class="{index % 2 === 0 ? 'timeline-start' : 'timeline-end'} timeline-box">
                                    <div class="flex flex-col items-center justify-center">
                                        {entry.name}
                                        <div>
                                            {#if entry.start || entry.end}
                                                {#if entry.start}
                                                    {new Date(entry.start).toLocaleTimeString([], {
                                                        hour: "2-digit",
                                                        minute: "2-digit",
                                                    })}
                                                {/if}
                                                {#if entry.start && entry.end}
                                                    -
                                                {/if}
                                                {#if entry.end}
                                                    {new Date(entry.end).toLocaleTimeString([], {
                                                        hour: "2-digit",
                                                        minute: "2-digit",
                                                    })}
                                                {/if}
                                            {/if}
                                        </div>
                                    </div>
                                </div>
                                <hr class="bg-accent" />
                            </li>
                        {/each}
                    </ul>
                </div>
            {/if}
        </div>
    </div>
</div>
