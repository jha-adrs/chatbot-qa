This is a [Next.js](https://nextjs.org/) project bootstrapped with [`create-next-app`](https://github.com/vercel/next.js/tree/canary/packages/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev

```
Create directories in data folder
```bash
cd data
mkdir processed
mkdir text
```
Now you need the packages listed in ```requirements.txt```
```
Without venv
pip install -r requirements.txt

Or with venv
python -v venv chatbot
pip install -r requirements.txt

Then, for windows:
./chatbot/scripts/activate

For Linux:
source /chatbot/bin/activate
```

Next, start context extractor 
and main.py
```
python context_extractor.py
python main.py
```
Done, Your Custom chatbot is ready!!
Note: Change your OpenAI config according to your plan, I am using the free plan so I have a timer to tackle the rate limit 3 req/min

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.
