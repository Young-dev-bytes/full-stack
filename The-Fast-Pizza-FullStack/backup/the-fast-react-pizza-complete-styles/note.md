key words:

> useLoaderData; createBrowserRouter; RouterProvider; useParams

### step one:

> npm create vite@4

### step two:

> install plugin : npm i eslint vite-plugin-eslint eslint-config-react-app --save-dev

### step three:

how to plan and build a react application

> FROM THE EARLIER “THINKING IN REACT” LECTURE:
> 1 Break the desired UI into components
> 2 Build a static version (no state yet)
> 3 Think about state management + data flow

👉 This works well for small apps with one page and a few features
👉 In real-world apps, we need to adapt this process

1 Gather application requirements and features
This is just a rough overview. In the real-world, things are never this linear
2 Divide the application into pages
👉 Thinkabouttheoverallandpage-levelUI
👉 BreakthedesiredUIintocomponents
👉 Designandbuildastaticversion(nostateyet)
3 Divide the application into feature categories
👉 Thinkaboutstatemanagement+dataflow
From earlier Fromearlier
From earlier
4 Decide on what libraries to use (technology decisions)

### step four:

move pages and features

### step five:

npm i react-router-dom@4

### step six:

install tailwind step by step
instal taildwind extension > Tailwind CSS IntelliSense
npm install -D prettier prettier-plugin-tailwindcss
config tailwindcss
{
"plugins": ["prettier-plugin-tailwindcss"],
"singleQuote": true
}

Video : Styling Form Elements
