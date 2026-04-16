<script lang="ts">
    import type { GuestGroupSchema, ResponseChoiceSchema, RsvpQuestionResponseSchema } from "$api-client";
    import AcceptedStats from "$lib/components/AcceptedStats.svelte";
    import InviteStats from "$lib/components/InviteStats.svelte";
    import RsvpStats from "$lib/components/RsvpStats.svelte";
    import Stats from "$lib/components/Stats.svelte";
    import ProtectedPageHeader from "$lib/components/layouts/ProtectedPageHeader.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";
    import { SvelteMap } from "svelte/reactivity";
    import type { IStat } from "../../../types";
    import type { PageData } from "./$types";

    const { data }: { data: PageData } = $props();
    const relativeCrumbs = [{ title: "Guest List", href: "/planning/guest_list" }, { title: "RSVP" }];

    // Build lookup map for guest groups
    const groupMap = $derived.by(() => {
        const map = new SvelteMap<string, GuestGroupSchema>();
        data.guestGroups.forEach((g) => map.set(g.id, g));
        return map;
    });

    // Build a submission -> guestGroupId lookup
    const submissionGroupMap = $derived.by(() => {
        const map = new SvelteMap<string, string>();
        data.submissions.forEach((s) => map.set(s.id, s.guestGroupId));
        return map;
    });

    type QuestionEntry = {
        questionId: string;
        questionText: string;
        questionType: string;
        questionOrder: number;
        answers: { group: GuestGroupSchema | null; response: RsvpQuestionResponseSchema }[];
    };

    // Group responses by question, sorted by question order
    const questionGroups = $derived.by(() => {
        const map = new SvelteMap<string, QuestionEntry>();
        data.responses.forEach((r) => {
            if (!r.questionId) return;
            if (!map.has(r.questionId)) {
                map.set(r.questionId, {
                    questionId: r.questionId,
                    questionText: r.questionText,
                    questionType: r.questionType,
                    questionOrder: r.questionOrder,
                    answers: [],
                });
            }
            const groupId = r.submissionId ? submissionGroupMap.get(r.submissionId) : undefined;
            const group = groupId ? (groupMap.get(groupId) ?? null) : null;
            map.get(r.questionId)!.answers.push({ group, response: r });
        });

        // Sort answers within each question by group name
        map.forEach((entry) => {
            entry.answers.sort((a, b) => (a.group?.name ?? "").localeCompare(b.group?.name ?? ""));
        });

        return Array.from(map.values()).sort((a, b) => a.questionOrder - b.questionOrder);
    });

    const statsValues: IStat[] = [
        {
            title: "Attending",
            value: data.stats.totalAttending,
            description: "Number of guests attending",
        },
        {
            title: "Declined",
            value: data.stats.totalDeclined,
            description: "Number of guests not attending",
        },
    ];

    const responseRate =
        data.stats.groupsInvited + data.stats.groupsAccepted + data.stats.groupsDeclined > 0
            ? Math.round(((data.stats.groupsAccepted + data.stats.groupsDeclined) / data.stats.groupsInvited) * 100)
            : 0;

    function formatResponseValue(r: RsvpQuestionResponseSchema): string {
        if (r.responseChoices && r.responseChoices.length > 0) {
            return r.responseChoices.map((c: ResponseChoiceSchema) => c.text).join(", ");
        }
        return r.responseText || "—";
    }
</script>

<ProtectedPageShell {relativeCrumbs}>
    <ProtectedPageHeader
        title="RSVP Responses"
        description="View all guest group RSVP submissions and their question responses."
        showButtons={false}>
    </ProtectedPageHeader>

    {#if data.submissions.length === 0}
        <div class="card bg-base-100 border border-base-300 shadow-lg">
            <div class="card-body items-center text-center py-16">
                <span class="icon-[lucide--mail-open] size-16 text-base-content/30 mb-4"></span>
                <h3 class="text-xl font-semibold text-base-content mb-2">No RSVP responses yet</h3>
                <p class="text-base-content/70 max-w-md">
                    Responses will appear here once guest groups have submitted their RSVPs.
                </p>
            </div>
        </div>
    {:else}
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 p-6">
            <div class="flex flex-col">
                <div class="card">
                    <div class="card-body items-center text-center">
                        <div class="card-title">Overall Response Rate</div>
                        <progress
                            class="progress progress-primary w-48"
                            value={responseRate}
                            max="100"
                            aria-valuenow={responseRate}
                            role="progressbar">
                            {responseRate}%
                        </progress>
                        <p class="text-sm text-accent-content mt-2">
                            {data.stats.groupsAccepted + data.stats.groupsDeclined} of {data.stats.groupsInvited} groups responded
                        </p>
                    </div>
                </div>
                <InviteStats rsvpStats={data.stats} layout="horizontal" />
            </div>
            <div class="flex flex-col">
                <RsvpStats rsvpStats={data.stats} layout="horizontal" />
                <AcceptedStats rsvpStats={data.stats} configData={data.configData} layout="horizontal" />
            </div>
        </div>
        {#if questionGroups.length === 0}
            <p class="text-accent bg-base-300 text-sm text-center py-8">No question responses recorded yet.</p>
        {:else}
            <div class="flex flex-col gap-2">
                {#each questionGroups as question (question.questionId)}
                    <div class="collapse collapse-arrow bg-base-300 text-accent border border-base-300">
                        <input type="checkbox" />
                        <div class="collapse-title font-semibold flex items-center gap-3">
                            <span>{question.questionText}</span>
                            <span class="badge badge-ghost badge-sm ml-auto mr-6">{question.answers.length}</span>
                        </div>
                        <div class="collapse-content">
                            <div class="overflow-x-auto">
                                <table class="table table-sm w-full">
                                    <thead>
                                        <tr>
                                            <th>Guest Group</th>
                                            <th>Answer</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {#each question.answers as { group, response } (response.id)}
                                            <tr>
                                                <td class="font-medium">
                                                    {#if group}
                                                        {group.name}
                                                    {:else}
                                                        <span class="italic">Unknown</span>
                                                    {/if}
                                                </td>
                                                <td>{formatResponseValue(response)}</td>
                                            </tr>
                                        {/each}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                {/each}
            </div>
        {/if}
    {/if}
</ProtectedPageShell>
