Users = [
    {'Username': 'Admin', 'Passcode': 'Admin123', 'Repeat_Preference': 5, 'Age_Category': '18-25', 'Gender': 'Female',
     'Focus_Area': "Work/Career", 'Suggestions': 3, 'Time_Available': 20, 'Level': 1, 'Score': 500, 'Streak': 0,
     'Days_Summed': 0, 'Role': 'Admin', 'Created_At': '2025-01-18 12:00:00'},
    {'Username': 'OpenAI', 'Passcode': 'OpenAI', 'Repeat_Preference': 5, 'Age_Category': '18-25', 'Gender': None,
     'Focus_Area': "Work/Career", 'Suggestions': 3, 'Time_Available': 20, 'Level': 1, 'Score': 500, 'Streak': 0,
     'Days_Summed': 0, 'Role': 'Admin', 'Created_At': '2025-01-18 12:00:00'}
]

Questionnaire = []

Questions = []

Status = []

Favorite = []

Recommendations_Per_Person = []

Records = []

Removed_Recommendations = []

Score_History = []

Recommendations = [

    {'ID': 1, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11", 
     'Title': '5-4-3-2-1 Grounding Exercise',
     'Description': 'Name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, and 1 you can taste to calm the nervous system quickly.',
     'Link': None, 'Points': 10},

    {'ID': 2, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11", 
     'Title': 'Dance It Out',
     'Description': 'Play 3 of your favorite songs and dance however you want. Shaking and moving helps release tension and boost your mood.',
     'Link': None, 'Points': 30},

    {'ID': 3, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11", 
     'Title': 'Journal Dump',
     'Description': 'Free-write for 10 minutes. Dump every thought onto paper without worrying about structure. Then tear it up if you want.',
     'Link': None, 'Points': 20},

    {'ID': 4, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11", 
     'Title': 'Box Breathing',
     'Description': 'Inhale for 4 seconds, hold for 4, exhale for 4, hold for 4. Repeat for 4 minutes to activate calm.',
     'Link': None, 'Points': 8},

    {'ID': 5, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11", 
     'Title': 'The “One Drawer” Reset',
     'Description': 'Choose one drawer or space and tidy or organize it while listening to calming music. Quick win, clear mind.',
     'Link': None, 'Points': 30},

    {'ID': 6, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11", 
     'Title': '3-Item Gratitude Shift',
     'Description': 'Write down three things that went right today or that you’re grateful for to boost perspective.',
     'Link': None, 'Points': 14},

    {'ID': 7, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11", 
     'Title': 'Shoulder and Jaw Release',
     'Description': 'Roll your shoulders slowly, then gently massage your jaw. Helps release hidden muscle tension from stress.',
     'Link': None, 'Points': 10},

    {'ID': 8, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11", 
     'Title': '20-Second Room Scan',
     'Description': 'Walk slowly through a room and observe details for 20 seconds at a time. Repeat for 5 minutes.',
     'Link': None, 'Points': 10},

    {'ID': 9, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11", 
     'Title': 'Silent Walk',
     'Description': 'Take a 10–15 minute walk without your phone or music. Observe the environment and your breathing.',
     'Link': None, 'Points': 30},

    {'ID': 10, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11", 
     'Title': 'Hand Over Heart Breathing',
     'Description': 'Place your hand over your heart, breathe slowly, and silently repeat, “I’m safe, I’m okay” for 5 minutes.',
     'Link': None, 'Points': 10},

    {'ID': 11, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11", 
     'Title': 'Letter to Your Younger Self',
     'Description': 'Spend 10–15 minutes writing a letter to your younger self. Say what you needed to hear then.',
     'Link': None, 'Points': 30},

    {'ID': 12, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11", 
     'Title': 'Tea Meditation',
     'Description': 'Make tea slowly and mindfully. Sit quietly while drinking it, focusing on warmth, scent, and taste.',
     'Link': None, 'Points': 30},

    {'ID': 13, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11", 
     'Title': 'Memory Visualization',
     'Description': 'Close your eyes and recall a peaceful memory. Imagine it in detail for 10 minutes to calm your mind.',
     'Link': None, 'Points': 20},

    {'ID': 14, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11", 
     'Title': 'Stretch and Sigh',
     'Description': 'Stretch neck, wrists, and ankles slowly. After each stretch, exhale with a big audible sigh to release tension.',
     'Link': None, 'Points': 20},

    {'ID': 15, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11", 
     'Title': 'Sing or Hum a Favorite Song',
     'Description': 'Sing or hum a song you love. Focus on breath and vibration. It soothes the nervous system naturally.',
     'Link': None, 'Points': 30},

    {'ID': 16, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11",
     'Title': 'Pelvic Tilt Stretch',
     'Description': 'Lie on your back with knees bent and feet flat. Tilt pelvis upward gently for 10 reps. Helps relieve tension from the lower back and hips, areas where stress often settles in female bodies.',
     'Link': None, 'Points': 10},

    {'ID': 17, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11",
     'Title': 'Womb-Centered Breathing',
     'Description': 'Sit comfortably and breathe deeply into your lower belly or womb space. Visualize warmth and release. This activates the parasympathetic system and calms cortisol responses common in female hormonal cycles.',
     'Link': None, 'Points': 10},

    {'ID': 18, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11",
     'Title': 'Gentle Hip Circles',
     'Description': 'Stand or sit and rotate hips slowly in circles. Helps release stress from the sacral region and reconnect with physical flow and breath.',
     'Link': None, 'Points': 10},

    {'ID': 19, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11",
     'Title': 'Upper Back Unwind',
     'Description': 'Use a wall or foam roller to stretch the upper back, where tension accumulates due to multitasking and emotional load-bearing often observed in women.',
     'Link': None, 'Points': 20},

    {'ID': 20, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11",
     'Title': 'Legs Up the Wall',
     'Description': 'Lie on your back with legs resting up a wall. Stay for 5–10 minutes. This relieves adrenal fatigue and improves lymph flow, which benefits hormonal stress regulation.',
     'Link': None, 'Points': 20},

    {'ID': 21, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11",
     'Title': 'Self-Compassion Mirror Exercise',
     'Description': 'Stand in front of a mirror, breathe deeply, and say something kind to yourself out loud. This helps counteract the internalized stress patterns common in female social conditioning.',
     'Link': None, 'Points': 10},

    {'ID': 22, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11",
     'Title': 'Progressive Muscle Burnout',
     'Description': 'Do a quick circuit: 15 push-ups, 20 squats, 30 seconds wall sit. Repeat 2x. This mimics a stress-response reset often effective for male bodies.',
     'Link': None, 'Points': 20},

    {'ID': 23, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11",
     'Title': 'Deep Chest Breathing',
     'Description': 'Stand tall, inhale deeply into your chest, hold for 3 seconds, exhale fully. Repeat 10 times. Helps open tight pecs and stabilize breath tension in male-dominant chest breathing patterns.',
     'Link': None, 'Points': 10},

    {'ID': 24, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11",
     'Title': 'Neck and Trap Release',
     'Description': 'Massage the upper traps and neck with firm, slow pressure or a massage ball. Male bodies often hold tension here from posture and adrenaline load.',
     'Link': None, 'Points': 10},

    {'ID': 25, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11",
     'Title': 'Punch-Out Visualization',
     'Description': 'Stand in fighter stance and slowly punch forward with intention while visualizing releasing tension. Repeat for 2–3 minutes. This channels physical stress out through focused movement.',
     'Link': None, 'Points': 10},

    {'ID': 26, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11",
     'Title': 'Cold Splash Reset',
     'Description': 'Splash cold water on your face or run wrists under cold water for 30 seconds. Resets the vagus nerve and reduces sympathetic overload often seen in high cortisol male bodies.',
     'Link': None, 'Points': 4},

    {'ID': 27, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11",
     'Title': 'Focused Breathing with Counting',
     'Description': 'Inhale for 4 seconds, exhale for 6 while counting down from 50. Directs analytical minds into bodily calm and diffuses overthinking stress patterns.',
     'Link': None, 'Points': 20},

    {'ID': 28, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11", 'Title': 'Microbreak Desk Stretch',
     'Description': 'Take a 5-minute break to stretch your arms, shoulders, and neck at your desk.',
     'Link': None, 'Points': 10},

    {'ID': 29, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11", 'Title': 'Task Sprint',
     'Description': 'Set a 10-minute timer and focus on completing a single small task to build momentum.',
     'Link': None, 'Points': 20},

    {'ID': 30, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11", 'Title': 'Declutter Your Inbox',
     'Description': 'Spend 15 minutes sorting, deleting, or responding to non-urgent emails.',
     'Link': None, 'Points': 30},

    {'ID': 31, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11", 'Title': 'Money Minute',
     'Description': 'Spend 5 minutes reviewing your budget or checking your bank app to regain control.',
     'Link': None, 'Points': 10},

    {'ID': 32, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11", 'Title': 'Subscription Sweep',
     'Description': 'In 10 minutes, list or cancel subscriptions you no longer use.',
     'Link': None, 'Points': 20},

    {'ID': 33, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11", 'Title': 'Gratitude over Spending',
     'Description': 'Write down 3 non-material things you’re grateful for instead of browsing online shops.',
     'Link': None, 'Points': 20},

    {'ID': 34, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11", 'Title': '10-Minute Yoga Flow',
     'Description': 'Follow a short online yoga session focused on releasing tension and calming the body.',
     'Link': None, 'Points': 20},

    {'ID': 35, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11", 'Title': 'Fruit + Water Reset',
     'Description': 'Drink a glass of water and eat a piece of fruit mindfully to refresh your body.',
     'Link': None, 'Points': 10},

    {'ID': 36, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11", 'Title': 'Breath Focus Body Scan',
     'Description': 'Lie or sit still for 15 minutes and mentally scan your body from head to toe.',
     'Link': None, 'Points': 30},

    {'ID': 37, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11", 'Title': 'Send a Thoughtful Message',
     'Description': 'Text someone you care about just to say you’re thinking of them.',
     'Link': None, 'Points': 10},

    {'ID': 38, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11", 'Title': 'Connection Check-In',
     'Description': 'Call a close friend or family member and ask how they’ve really been.',
     'Link': None, 'Points': 30},

    {'ID': 39, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11", 'Title': 'List People Who Lift You',
     'Description': 'Write a list of people who energize you, and reflect on how they support your joy.',
     'Link': None, 'Points': 20},

    {'ID': 40, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11", 'Title': 'Mini Priority Sort',
     'Description': 'Write down 3 top priorities for today and cross off low-urgency distractions.',
     'Link': None, 'Points': 16},

    {'ID': 41, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11", 'Title': 'The 2-Minute Rule',
     'Description': 'If a task will take less than 2 minutes, do it now. Set a 10-minute timer.',
     'Link': None, 'Points': 20},

    {'ID': 42, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11", 'Title': 'Pomodoro Reset',
     'Description': 'Do one 15-minute focus session on a task you\'ve been putting off.',
     'Link': None, 'Points': 30},

    {'ID': 43, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11", 'Title': 'Mirror Affirmation',
     'Description': 'Look at yourself and say three kind things out loud. Repeat them for 5 minutes.',
     'Link': None, 'Points': 10},

    {'ID': 44, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11", 'Title': 'Write Your Superpowers',
     'Description': 'List your strengths or proud moments for 10 minutes, however big or small.',
     'Link': None, 'Points': 20},

    {'ID': 45, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11", 'Title': 'Values Check',
     'Description': 'Write down your top 5 values and one small way to live them today.',
     'Link': None, 'Points': 20},

    {'ID': 46, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11", 'Title': 'Create a “Knowns” List',
     'Description': 'List what you *do* know or control right now. Helps ease chaos.',
     'Link': None, 'Points': 20},

    {'ID': 47, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11", 'Title': 'Tiny Timeline',
     'Description': 'Make a 10-minute visual map of what’s coming this week, day-by-day.',
     'Link': None, 'Points': 20},

    {'ID': 48, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11", 'Title': 'Future Self Note',
     'Description': 'Write a note to your future self a year from now, offering encouragement.',
     'Link': None, 'Points': 20},

    {'ID': 49, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11", 'Title': 'Screen-Free Reset',
     'Description': 'Put your phone down and set a 15-minute timer for a no-screen break.',
     'Link': None, 'Points': 30},

    {'ID': 50, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11", 'Title': 'Unfollow Cleanse',
     'Description': 'Unfollow 10 accounts that cause stress or comparison on your social feeds.',
     'Link': None, 'Points': 16},

    {'ID': 51, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11", 'Title': 'Analog Minute',
     'Description': 'Write something with a pen and paper—a list, a doodle, a note—for 10 minutes.',
     'Link': None, 'Points': 20},

    {'ID': 52, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11", 'Title': 'Worst Case / Best Case',
     'Description': 'List your fear, then write the best and worst case outcomes and a response plan.',
     'Link': None, 'Points': 20},

    {'ID': 53, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11", 'Title': '1-Year Vision Sketch',
     'Description': 'Draw or describe your life one year from now. Focus on hope, not details.',
     'Link': None, 'Points': 20},

    {'ID': 54, 'Passcode': 'Admin123', 'Created_At': "2025-06-09 16:25:11", 'Title': '3 Small Steps',
     'Description': 'Break a big fear into 3 tiny doable steps and write them down.',
     'Link': None, 'Points': 20},

    {
        'ID': 56,
        'Passcode': 'Admin123',
        'Created_At': '2025-06-09 16:25:11',
        'Title': 'Gratitude Glance',
        'Description': "Take a moment to write down three things you're grateful for. They can be big (a relationship, a life change) or small (warm socks, the smell of coffee). Gratitude gently rewires your brain toward positivity and reinforces the good moments.",
        'Link': None,
        'Points': 10
    },

    {
        'ID': 57,
        'Passcode': 'Admin123',
        'Created_At': '2025-06-09 16:25:11',
        'Title': 'Sunlight Sip',
        'Description': "Grab a cup of tea, coffee, or water and sit by a window or step outside. Let the sunlight (or just daylight) hit your skin while you slowly sip. No multitasking — just breathe and notice the world around you. This small pause keeps your nervous system regulated.",
        'Link': None,
        'Points': 20
    },

    {
        'ID': 58,
        'Passcode': 'Admin123',
        'Created_At': '2025-06-09 16:25:11',
        'Title': 'Micro-Adventure',
        'Description': "Leave your usual environment and go for a short walk — even just around the block. Let curiosity guide you: notice details you’ve never really seen before. Shifting your physical space resets your mental state and boosts creativity.",
        'Link': None,
        'Points': 30
    },

    {
        'ID': 59,
        'Passcode': 'Admin123',
        'Created_At': '2025-06-09 16:25:11',
        'Title': 'Stretch & Breathe',
        'Description': "Stand up and do three easy stretches — reach your arms overhead, bend forward, roll your shoulders. Match your movement with deep, slow breaths. Even light physical movement can shift your body out of stress mode.",
        'Link': None,
        'Points': 14
    },

    {
        'ID': 60,
        'Passcode': 'Admin123',
        'Created_At': '2025-06-09 16:25:11',
        'Title': 'Sound Reset',
        'Description': "Put on headphones and play something calming — nature sounds, instrumental music, a favorite mellow song. Sit or lie down, close your eyes, and give the music your full attention. This anchors you in the present and slows racing thoughts.",
        'Link': None,
        'Points': 20
    },

    {
        'ID': 61,
        'Passcode': 'Admin123',
        'Created_At': '2025-06-09 16:25:11',
        'Title': 'Mindful Savor',
        'Description': "Choose a snack or drink and experience it as if for the first time. Eat slowly, noticing the taste, smell, texture, and temperature. Let this be your only task. When you fully experience something small, it tells your brain you're safe.",
        'Link': None,
        'Points': 20
    },

    {
        'ID': 62,
        'Passcode': 'Admin123',
        'Created_At': '2025-06-09 16:25:11',
        'Title': '5-4-3-2-1 Grounding',
        'Description': "Engage your senses to return to the here and now: name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, and 1 you can taste. This is a reliable tool for anxiety, especially when thoughts start spiraling.",
        'Link': None,
        'Points': 16
    },

    {
        'ID': 63,
        'Passcode': 'Admin123',
        'Created_At': '2025-06-09 16:25:11',
        'Title': 'Tidy a Corner',
        'Description': "Choose one small space — your desk, your bed, your backpack — and tidy it up. Physical organization sends a signal to your brain that you’re regaining control. Don’t worry about perfection. Just reset one spot.",
        'Link': None,
        'Points': 30
    },

    {
        'ID': 64,
        'Passcode': 'Admin123',
        'Created_At': '2025-06-09 16:25:11',
        'Title': 'Guided Mini-Meditation',
        'Description': "Use a free app (like Insight Timer or Headspace) or a YouTube video to do a short guided meditation focused on calming breath or body awareness. Let someone else guide your mind so you don’t have to direct it yourself.",
        'Link': 'https://insighttimer.com/',
        'Points': 20
    },

    {
        'ID': 65,
        'Passcode': 'Admin123',
        'Created_At': '2025-06-09 16:25:11',
        'Title': 'Box Breathing',
        'Description': "Use this proven breathing technique used by Navy SEALs and therapists alike: Inhale for 4 seconds, hold for 4, exhale for 4, hold for 4. Repeat for 4–6 cycles. This regulates your nervous system and creates an immediate sense of calm.",
        'Link': None,
        'Points': 12
    },

    {
        'ID': 66,
        'Passcode': 'Admin123',
        'Created_At': '2025-06-09 16:25:11',
        'Title': 'Cold Reset',
        'Description': "Run cold water over your wrists or splash your face. Hold something cold — like a chilled spoon or ice pack. This activates the dive reflex and forces your body to slow down, interrupting panic or overestimation.",
        'Link': None,
        'Points': 10
    },

    {
        'ID': 67,
        'Passcode': 'Admin123',
        'Created_At': '2025-06-09 16:25:11',
        'Title': 'Body Shake-Out',
        'Description': "Turn on music and shake your limbs — arms, legs, shoulders — like you’re shaking off tension. You can even jump in place or do a few jumping jacks. When your body moves, your stress has somewhere to go.",
        'Link': None,
        'Points': 20
    },

    {
        'ID': 68,
        'Passcode': 'Admin123',
        'Created_At': '2025-06-09 16:25:11',
        'Title': 'Quiet Cave',
        'Description': "Find a quiet, low-stimulation space. Turn off notifications. Dim the lights or close your eyes. Wrap yourself in a blanket or hoodie. For these few minutes, let yourself rest with no demands. Sometimes, doing nothing is the most healing choice.",
        'Link': None,
        'Points': 30
    },

    {
        'ID': 69,
        'Passcode': 'Admin123',
        'Created_At': '2025-06-09 16:25:11',
        'Title': 'Emergency Journal Dump',
        'Description': "Grab paper or open a blank document. Set a timer. Write everything that’s in your head — messy, raw, unfiltered. Don’t worry about grammar or logic. Just get it out. You can burn or delete it afterward if you want.",
        'Link': None,
        'Points': 20
    },

    {
        'ID': 55,
        'Passcode': 'Admin123',
        'Created_At': '2025-06-09 16:25:11',
        'Title': 'Name 3 Safe Things',
        'Description': "Aloud or silently, name three things that are safe and stable in your life — a friend who cares, your favorite hoodie, your breath. Say them again. And again. This creates a mental “anchor” when you feel like you're slipping.",
        'Link': None,
        'Points': 10
    }


]

Tags = [
    {'ID': 1, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Age Variant', 'Category': '19–25', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 2, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Age Variant', 'Category': '19–25', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 3, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Age Variant', 'Category': '19–25', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 4, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Age Variant', 'Category': '26–35', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 5, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Age Variant', 'Category': '26–35', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 6, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Age Variant', 'Category': '26–35', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 7, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Age Variant', 'Category': '36–55', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 8, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Age Variant', 'Category': '36–55', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 9, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Age Variant', 'Category': '36–55', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 10, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Age Variant', 'Category': '56–70', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 11, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Age Variant', 'Category': '56–70', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 12, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Age Variant', 'Category': '56–70', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 13, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Age Variant', 'Category': '70+', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 14, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Age Variant', 'Category': '70+', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 15, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Age Variant', 'Category': '70+', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 1, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 5, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 2, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 15, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 3, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 10, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 4, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 4, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 5, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 15, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 6, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 7, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 7, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 5, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 8, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 5, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 9, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 15, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 10, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 5, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 11, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 15, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 12, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 15, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 13, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 10, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 14, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 10, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 15, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 15, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 16, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Gender', 'Category': 'Female', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 16, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 5, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 17, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Gender', 'Category': 'Female', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 17, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 5, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 18, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Gender', 'Category': 'Female', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 18, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 5, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 19, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Gender', 'Category': 'Female', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 19, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 10, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 20, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Gender', 'Category': 'Female', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 20, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 10, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 21, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Gender', 'Category': 'Female', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 21, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 5, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 22, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Gender', 'Category': 'Male', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 22, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 10, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 23, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Gender', 'Category': 'Male', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 23, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 5, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 24, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Gender', 'Category': 'Male', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 24, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 5, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 25, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Gender', 'Category': 'Male', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 25, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 5, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 26, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Gender', 'Category': 'Male', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 26, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 2, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 27, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Gender', 'Category': 'Male', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 27, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 10, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 28, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Area of Focus', 'Category': 'Work/Career', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 28, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 5, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 29, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Area of Focus', 'Category': 'Work/Career', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 29, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 10, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 30, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Area of Focus', 'Category': 'Work/Career', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 30, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 15, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 31, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Area of Focus', 'Category': 'Finances', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 31, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 5, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 32, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Area of Focus', 'Category': 'Finances', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 32, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 10, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 33, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Area of Focus', 'Category': 'Finances', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 33, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 10, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 34, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Area of Focus', 'Category': 'Health & Well-being', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 34, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 10, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 35, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Area of Focus', 'Category': 'Health & Well-being', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 35, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 5, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 36, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Area of Focus', 'Category': 'Health & Well-being', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 36, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 15, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 37, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Area of Focus', 'Category': 'Relationships', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 37, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 5, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 38, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Area of Focus', 'Category': 'Relationships', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 38, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 15, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 39, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Area of Focus', 'Category': 'Relationships', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 39, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 10, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 40, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Area of Focus', 'Category': 'Time Management', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 40, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 8, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 41, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Area of Focus', 'Category': 'Time Management', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 41, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 10, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 42, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Area of Focus', 'Category': 'Time Management', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 42, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 15, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 43, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Area of Focus', 'Category': 'Personal Identity', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 43, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 5, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 44, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Area of Focus', 'Category': 'Personal Identity', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 44, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 10, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 45, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Area of Focus', 'Category': 'Personal Identity', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 45, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 10, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 46, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Area of Focus', 'Category': 'Major Life Changes', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 46, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 10, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 47, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Area of Focus', 'Category': 'Major Life Changes', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 47, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 10, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 48, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Area of Focus', 'Category': 'Major Life Changes', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 48, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 10, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 49, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Area of Focus', 'Category': 'Social Media & Technology', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 49, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 15, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 50, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Area of Focus', 'Category': 'Social Media & Technology', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 50, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 8, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 51, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Area of Focus', 'Category': 'Social Media & Technology', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 51, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 10, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 52, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Area of Focus', 'Category': 'Uncertainty & Future Planning', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 52, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 10, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 53, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Area of Focus', 'Category': 'Uncertainty & Future Planning', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 53, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 10, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 54, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Area of Focus', 'Category': 'Uncertainty & Future Planning', 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 54, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 10, 'Created_At': "2025-06-09 16:25:11"},
    {'ID': 56, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Stress Level', 'Category': 0, 'Created_At': '2025-06-09 16:25:11'},
    {'ID': 57, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Stress Level', 'Category': 0, 'Created_At': '2025-06-09 16:25:11'},
    {'ID': 58, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Stress Level', 'Category': 0, 'Created_At': '2025-06-09 16:25:11'},
    {'ID': 59, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Stress Level', 'Category': 1, 'Created_At': '2025-06-09 16:25:11'},
    {'ID': 60, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Stress Level', 'Category': 1, 'Created_At': '2025-06-09 16:25:11'},
    {'ID': 61, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Stress Level', 'Category': 1, 'Created_At': '2025-06-09 16:25:11'},
    {'ID': 62, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Stress Level', 'Category': 2, 'Created_At': '2025-06-09 16:25:11'},
    {'ID': 63, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Stress Level', 'Category': 2, 'Created_At': '2025-06-09 16:25:11'},
    {'ID': 64, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Stress Level', 'Category': 2, 'Created_At': '2025-06-09 16:25:11'},
    {'ID': 65, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Stress Level', 'Category': 3, 'Created_At': '2025-06-09 16:25:11'},
    {'ID': 66, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Stress Level', 'Category': 3, 'Created_At': '2025-06-09 16:25:11'},
    {'ID': 67, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Stress Level', 'Category': 3, 'Created_At': '2025-06-09 16:25:11'},
    {'ID': 68, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Stress Level', 'Category': 4, 'Created_At': '2025-06-09 16:25:11'},
    {'ID': 69, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Stress Level', 'Category': 4, 'Created_At': '2025-06-09 16:25:11'},
    {'ID': 55, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Stress Level', 'Category': 4, 'Created_At': '2025-06-09 16:25:11'},
    {'ID': 56, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 5, 'Created_At': '2025-06-09 16:25:11'},
    {'ID': 57, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 10, 'Created_At': '2025-06-09 16:25:11'},
    {'ID': 58, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 15, 'Created_At': '2025-06-09 16:25:11'},
    {'ID': 59, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 7, 'Created_At': '2025-06-09 16:25:11'},
    {'ID': 60, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 10, 'Created_At': '2025-06-09 16:25:11'},
    {'ID': 61, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 10, 'Created_At': '2025-06-09 16:25:11'},
    {'ID': 62, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 8, 'Created_At': '2025-06-09 16:25:11'},
    {'ID': 63, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 15, 'Created_At': '2025-06-09 16:25:11'},
    {'ID': 64, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 10, 'Created_At': '2025-06-09 16:25:11'},
    {'ID': 65, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 6, 'Created_At': '2025-06-09 16:25:11'},
    {'ID': 66, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 5, 'Created_At': '2025-06-09 16:25:11'},
    {'ID': 67, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 10, 'Created_At': '2025-06-09 16:25:11'},
    {'ID': 68, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 15, 'Created_At': '2025-06-09 16:25:11'},
    {'ID': 69, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 10, 'Created_At': '2025-06-09 16:25:11'},
    {'ID': 55, 'Passcode': 'Admin123', 'Title_Of_Criteria': 'Time Available', 'Category': 5, 'Created_At': '2025-06-09 16:25:11'}
]
