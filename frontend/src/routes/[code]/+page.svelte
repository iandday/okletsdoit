<script lang="ts">
    import type { PageData } from "./$types";

    let { data }: { data: PageData } = $props();
</script>

<div class="container mx-auto max-w-4xl p-6">
    <div class="card bg-base-100 card-border">
        <div class="card-body">
            <h1 class="card-title text-3xl">Welcome, {data.guestGroup.name}!</h1>

            <div class="divider"></div>

            <div class="space-y-4">
                <div>
                    <p class="text-sm opacity-70">RSVP Code</p>
                    <p class="text-xl font-mono">{data.rsvpCode}</p>
                </div>

                <div class="stats stats-vertical lg:stats-horizontal shadow">
                    <div class="stat">
                        <div class="stat-title">Group Size</div>
                        <div class="stat-value text-primary">{data.guestGroup.group_count}</div>
                        <div class="stat-desc">Total guests in your party</div>
                    </div>

                    <div class="stat">
                        <div class="stat-title">Invited</div>
                        <div class="stat-value text-secondary">{data.guestGroup.group_invited_count}</div>
                        <div class="stat-desc">Guests invited</div>
                    </div>

                    <div class="stat">
                        <div class="stat-title">Status</div>
                        <div class="stat-value text-accent">
                            {#if data.guestGroup.group_attending_count > 0}
                                Attending
                            {:else if data.guestGroup.group_declined_count > 0}
                                Declined
                            {:else}
                                Pending
                            {/if}
                        </div>
                    </div>
                </div>

                {#if data.guestGroup.notes}
                    <div class="alert alert-info">
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            fill="none"
                            viewBox="0 0 24 24"
                            class="h-6 w-6 shrink-0 stroke-current">
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="2"
                                d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                        <span>{data.guestGroup.notes}</span>
                    </div>
                {/if}

                <div class="card-actions justify-end">
                    <a href="/rsvp" class="btn btn-primary"> Continue to RSVP </a>
                </div>
            </div>
        </div>
    </div>
</div>
