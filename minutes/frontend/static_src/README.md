# django-minutes-frontend

## Development

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Integration while development

To have a frictionless developer experience while developing this frontend we make use of the 
[proxy feature in create-react-app](https://create-react-app.dev/docs/proxying-api-requests-in-development/).  
If you have your django development server running on `localhost:8000` it will relay all calls to it, making it superconvenient to 
develop against the API.

### Integration for production

Django needs the generated `index.html` from this build to be in the templates, while all assets
need to go into the `static` folder of the `minutes.frontend` app. Doing a `npm run build` will take 
care of this automatically, as there is a `postbuild` step configured in `package.json`.
```json
  [...]
  "scripts": {
    [...]
    "postbuild": "rm -R ../static/app; mkdir -p ../static/app; cp -R build/* ../static/app &&  cp build/index.html ../templates/minutes/frontend/",
    [...]
  },
  [...]
  
```
Be sure to execute `npm run build` after every change to the frontend, otherwise these changes won't be reflected on
the production application.

### Available Scripts

In the project directory, you can run:

#### `npm start`

Runs the app in the development mode.<br />
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.<br />
You will also see any lint errors in the console.

#### `npm test`

Launches the test runner in the interactive watch mode.<br />
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

#### `npm run build`

Builds the app for production to the `build` folder.<br />
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.<br />
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

#### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can’t go back!**

If you aren’t satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you’re on your own.

You don’t have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn’t feel obligated to use this feature. However we understand that this tool wouldn’t be useful if you couldn’t customize it when you are ready for it.
