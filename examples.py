"""Pre-loaded example transcripts for quick demos covering math, tutorials, and general topics."""

EXAMPLES = {
    "(none)": "",

    # ===== MATH =====
    "Math: Quick intro to derivatives": (
        "Today we're going to talk about derivatives. A derivative measures how a function "
        "changes as its input changes. If we have a function f of x equals x squared, then "
        "the derivative is two x. The way we get this is by taking the limit as h approaches "
        "zero of f of x plus h minus f of x, all divided by h. Let's do a dry run. Take f of "
        "x equals x squared at x equals three. The derivative is two times three, which is six. "
        "That means at x equals three, the function is increasing at a rate of six units per "
        "unit. This concept is foundational for calculus and shows up everywhere in physics, "
        "engineering, and machine learning. Common mistake: forgetting that the derivative of "
        "a constant is zero, not the constant itself."
    ),
    "Math: Pythagorean theorem proof": (
        "The Pythagorean theorem states that in a right triangle, a squared plus b squared "
        "equals c squared, where c is the hypotenuse. One elegant proof uses similar triangles. "
        "Draw a right triangle ABC with the right angle at C. Drop a perpendicular from C to "
        "the hypotenuse AB, calling the foot H. This creates two smaller triangles, both "
        "similar to the original. From similarity, we get the ratios that yield a squared "
        "equals AH times AB, and b squared equals BH times AB. Adding these: a squared plus "
        "b squared equals AB times the quantity AH plus BH, which equals AB squared, which "
        "is c squared. Worked example: in a triangle with legs 3 and 4, the hypotenuse is "
        "the square root of 9 plus 16, which is the square root of 25, which equals 5."
    ),
    "Math: Bayes theorem intuition": (
        "Bayes theorem tells us how to update our beliefs with new evidence. The formula is: "
        "P of A given B equals P of B given A times P of A all divided by P of B. The intuition "
        "is that the probability of a hypothesis A being true, given that we observed evidence B, "
        "depends on how likely the evidence would be if A were true, weighted by how likely A "
        "was to begin with. Worked example: suppose a disease affects 1 in 1000 people. A test "
        "is 99 percent accurate. If someone tests positive, what is the probability they "
        "actually have the disease? Many people answer 99 percent. The correct answer using "
        "Bayes is roughly 9 percent. The low base rate dominates the result. This is the "
        "base rate fallacy and it appears constantly in medical testing and machine learning."
    ),

    # ===== TUTORIAL =====
    "Tutorial: Setting up a Python project": (
        "In this tutorial we'll set up a Python project from scratch. First, install Python "
        "3.11 from python.org. Then open your terminal and run python dash m venv venv to "
        "create a virtual environment. Activate it with source venv slash bin slash activate "
        "on Mac or Linux, or venv backslash Scripts backslash activate on Windows. Next, "
        "create a requirements dot txt file listing your dependencies, then run pip install "
        "dash r requirements dot txt. A common pitfall is forgetting to activate the venv "
        "before installing packages, which pollutes your global Python install. Always "
        "verify your prompt shows the venv name in parentheses."
    ),
    "Tutorial: Git basics": (
        "Git is a version control system used by millions of developers. To start, install "
        "git from git-scm.com. Inside a project folder, run git init to create a repository. "
        "Use git add filename to stage changes and git commit dash m to commit them with a "
        "message. Push to GitHub with git remote add origin and git push origin main. The "
        "key concepts are working directory, staging area, and repository. A common mistake "
        "is committing secrets like API keys. Always add a dot gitignore file with sensitive "
        "paths before your first commit. To check status, use git status. To see history, "
        "use git log."
    ),
    "Tutorial: Hello World in Rust": (
        "Let's write Hello World in Rust. First install Rust from rustup.rs. The command "
        "rustup will download both the compiler rustc and the package manager cargo. Create "
        "a new project with cargo new hello_world. This generates a folder with a src "
        "directory containing main.rs. Open main.rs and you'll see fn main with println bang "
        "hello world. The bang indicates println is a macro, not a function. Compile and run "
        "with cargo run. Cargo handles building, dependency management, and testing. A common "
        "beginner mistake is confusing macros with functions because both look like calls."
    ),

    # ===== GENERAL =====
    "General: Why sleep matters": (
        "Sleep is one of the most underrated aspects of human health. Adults need seven to "
        "nine hours of sleep per night for optimal cognitive function. During deep sleep, "
        "the brain clears out metabolic waste through the glymphatic system. Chronic sleep "
        "deprivation is linked to increased risk of heart disease, diabetes, depression, and "
        "even Alzheimer's. The most impactful thing you can do is keep a consistent sleep "
        "schedule, avoid screens for an hour before bed, and keep your room cool and dark. "
        "Caffeine has a half-life of around six hours, so avoid it after lunch if you "
        "struggle to fall asleep. Quality matters more than quantity."
    ),
    "General: Compound interest explained": (
        "Compound interest is often called the eighth wonder of the world. It is interest "
        "calculated not just on the principal, but also on accumulated interest. If you "
        "invest 1000 dollars at 10 percent annually, after one year you have 1100. After "
        "two years you have 1210, not 1200, because the second year you also earn interest "
        "on the 100 from the first year. Over 30 years at 10 percent, 1000 becomes about "
        "17449. The key takeaway is that time is the most important variable. Starting at "
        "age 25 with small contributions beats starting at age 40 with large contributions. "
        "The same principle applies in reverse for debt: credit card balances compound "
        "against you. Pay them off aggressively."
    ),
    "General: How vaccines work": (
        "Vaccines work by training your immune system to recognize and fight a specific "
        "pathogen without you having to get the actual disease first. Most vaccines contain "
        "either a weakened virus, a killed virus, a piece of the virus like a protein, or "
        "the genetic instructions for your cells to make that protein, which is how mRNA "
        "vaccines work. Once your immune system sees the antigen, it produces antibodies and "
        "memory cells. If you encounter the real pathogen later, your immune system mounts a "
        "fast targeted response. Side effects like a sore arm or mild fever are signs the "
        "immune system is working. They are not the disease. Vaccines have prevented an "
        "estimated 154 million deaths over the last 50 years."
    ),
}


def get_example_names():
    return list(EXAMPLES.keys())


def get_example_text(name: str) -> str:
    return EXAMPLES.get(name, "")
