<script>
import dayjs from 'dayjs';
import {
    onMount,
    onDestroy
} from 'svelte';

let date = dayjs();

let month = date.month();
let year = date.year();
let dates = Array(dayjs(`${year}-${month + 1}`, 'YYYY-MM').daysInMonth())
    .fill()
    .map((_, i) => dayjs(`${year}-${month + 1}-${i + 1}`, 'YYYY-MM-DD'));

let preElement;
let editable = true;
let isDirty = false;
let savedJournalEntry = '';
let selectedDate;
let showAlert = false;

let journalEntry = '';
let showJournal = false;

async function getJournalEntry(date) {
    try {
        if (dayjs(date).isAfter(dayjs())) {
            showAlert = "You can't select a future date.";
            return;
        }

        const response = await fetch(`http://localhost:8001/journal/${date}`);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        if (data.message) {
            await createJournalEntry(date);
            journalEntry = '';
        } else {
            journalEntry = data;
        }

        showJournal = true;
        savedJournalEntry = journalEntry;
        selectedDate = date;
    } catch (error) {
        console.error("An error occurred while fetching the journal entry:", error);
        showAlert = error.message || "An error occurred. Please try again later.";
    }
}

async function saveJournalEntry() {
    try {
        const entryText = preElement.value;  // Using value property instead of textContent
        const response = await fetch(`http://localhost:8001/journal/${selectedDate}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                date: selectedDate,
                entry: entryText
            }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        isDirty = false;
        savedJournalEntry = entryText; // Save the updated entry
    } catch (error) {
        console.error("An error occurred while saving the journal entry:", error);
        showAlert = error.message || "An error occurred. Please try again later.";
    }
}


async function createJournalEntry(date) {
    try {
        const response = await fetch(`http://localhost:8001/journal/${date}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                date: date,
                entry: ""
            }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        journalEntry = data;
    } catch (error) {
        console.error("An error occurred while creating the journal entry:", error);
        showAlert = error.message || "An error occurred. Please try again later.";
    }
}

async function updateEntry(e) {
    const currentEntry = document.querySelector('.journal-entry').textContent;
    if (isDirty) {
        if (confirm('This has been modified but not saved. Are you sure you want to exit without saving?')) {
            journalEntry = savedJournalEntry;
            preElement.textContent = savedJournalEntry;
        } else {
            return;
        }
    }
    savedJournalEntry = currentEntry;
    isDirty = false;
}

function onInput(e) {
    isDirty = e.target.value !== savedJournalEntry;
    if (e.target.value.length > 1000) {
        e.target.value = e.target.value.substring(0, 1000);
    } else {
        journalEntry = e.target.value; // Update journalEntry with the current content.
    }
}

let onKeyUpHandler = (e) => {
    if (e.key === 'Escape') {
        updateEntry(e);
    }
};

onMount(() => {
    window.addEventListener('keyup', onKeyUpHandler);
});

onDestroy(() => {
    window.removeEventListener('keyup', onKeyUpHandler);
});
</script>

<div class="app-container">
    <main>

        <div class="calendar">
            <table>
                <thead>
                    <tr>
                        <th>Sat</th>
                        <th>Sun</th>
                        <th>Mon</th>
                        <th>Tue</th>
                        <th>Wed</th>
                        <th>Thu</th>
                        <th>Fri</th>

                    </tr>
                </thead>
                <tbody>
                    <!-- Create a new row for each week -->
                    {#each [0, 7, 14, 21, 28] as startOfWeek}
                    <tr>
                        <!-- Create a new cell for each day of the week -->
                        {#each [0, 1, 2, 3, 4, 5, 6] as dayOfWeek}
                        <!-- Update the calendar markup to disable future dates -->
                        {#if dates[startOfWeek + dayOfWeek]}
                        <td>
                            <button class="date-container {dates[startOfWeek + dayOfWeek].format('YYYY-MM-DD') === selectedDate ? 'selected' : ''}"
                                on:click={() => {
                                selectedDate = dates[startOfWeek + dayOfWeek].format('YYYY-MM-DD');
                                getJournalEntry(selectedDate);
                                }}
                                disabled={dayjs(dates[startOfWeek + dayOfWeek].format('YYYY-MM-DD')).isAfter(dayjs())}>

                                {dates[startOfWeek + dayOfWeek].format('DD')}
                            </button>
                        </td>
                        {:else}
                        <td></td>
                        {/if}
                        {/each}
                    </tr>
                    {/each}
                </tbody>
            </table>
        </div>

        {#if showAlert}
        <div class="alert">{showAlert}</div>
        {/if}

        {#if showJournal}
        <div class="journal-container">
            <div>
                <textarea bind:this={preElement} class="journal-entry" bind:value={journalEntry} on:input={onInput} />
            </div>
            <div class="button-count-container">
                <div class="character-count">{journalEntry.length}/1000</div>
                <!-- <button class="save-button" on:click={() => saveJournalEntry(document.querySelector('.journal-entry').textContent)}>Save</button> -->
                <button class="save-button" on:click={saveJournalEntry}>Save</button>

            </div>
        </div>
        
            
        {/if}

    </main>
</div>

<!-- Your CSS here -->

<style>
.app-container {
    background-color: #282828;
    height: 100vh;
    width: 100vw;
    position: fixed;
    top: 0;
    left: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow-y: auto;
}

.calendar {
    width: 400px;
    margin-bottom: 2em;
    /* Adds some space between the calendar and the textarea */
}

main {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.date-container {
    border: 1px solid black;
    display: inline-block;
    padding: 1em;
    margin-bottom: 1em;
    background-color: aliceblue;
    color: black;
}

.date-container:hover {
    background-color: yellowgreen;
    color: white;
    cursor: pointer;
}

.date-container.selected {
    background-color: yellowgreen;
    /* change to any color you like */
}

.journal-container {
    padding: 1em;
    position: relative;
    border: solid 1px violet;
}

.journal-entry {
    color: yellowgreen;
    padding: 1em;
    white-space: pre-wrap;
    text-align: left;
    width: 600px;
    /* height: 320px; */
    min-height: 120px;
    border: none;
    background: transparent;
    overflow: auto;
    outline: none;
    resize: none;
    font-family: monospace;
}

th {
    color: ghostwhite;
}

.button-count-container {
    position: absolute;
    /* bottom: 10px; */
    left: 10px;
    display: flex;
    align-items: center;
    gap: 10px; /* space between the button and the character count */
}

.save-button {
    position: absolute;
    color: ghostwhite;
    /* left: 50px; */
    font-size: 0.8em; 
    background-color: rgba(0,0,0,0.5); 
    padding: 5px 10px; /* increase horizontal padding to give it a more button-like shape */
    border-radius: 5px; 
    border: none;
    cursor: pointer;
    
    transition: background-color 0.3s ease; /* transition for hover effect */
}

.save-button:hover {
    background-color: rgba(0,0,0,0.7); /* darken button on hover */
}


.character-count {
    position: absolute;
    left: 10px; /* align it with the left edge */
    bottom: 10px; 
    color: ghostwhite;
    font-size: 0.8em; 
    background-color: rgba(0,0,0,0.5); 
    padding: 5px;
    border-radius: 5px; 
}

@media (min-width: 640px) {
    main {
        max-width: none;
    }
}
</style>
