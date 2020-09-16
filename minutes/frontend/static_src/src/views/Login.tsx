import React, {ChangeEvent, FormEvent, useState} from 'react';
import {useHistory} from 'react-router'
import {Button, Card, Classes, Elevation, InputGroup} from "@blueprintjs/core";
import {observer} from "mobx-react";
import {useStores} from "../store";
import {createApiClient} from "../api/client";
import {TokenSet} from "../api/models/TokenSet";
import {idToRoute, RouteId} from "../routes";
import styles from './Login.module.scss';
import {MINIMAL} from "@blueprintjs/core/lib/esm/common/classes";

function Login(): JSX.Element {
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [errors, setErrors] = useState<Array<string>>([])
    const history = useHistory();
    const stores = useStores()
    const login = async (event: FormEvent) => {
        event.preventDefault()
        const authApi = createApiClient().authApi
        try {
            setErrors([])
            const tokenSet = await authApi.createTokenSetByCredentials({
                tokenUserCredentials: {
                    username: username,
                    password: password
                }
            })
            stores.credentials.setTokenSet(tokenSet as TokenSet)
            history.push(idToRoute(RouteId.MEETING_SERIES).path)
        } catch (e) {
            setErrors(['Invalid credentials'])
        }
    }

    const handleInputChange = (event: ChangeEvent<HTMLInputElement>) => {
        const target = event.target
        const value = target.value
        const name = target.name
        switch (name) {
            case 'username':
                setUsername(value)
                break
            case 'password':
                setPassword(value)
                break
        }
    }

    const ErrorsDisplay = function () {
        return (
            <div className='d-flex'>
                {errors.map(item => <span key={item} className={`${Classes.INTENT_DANGER} error-message`}>{item}</span>)}
            </div>
        )
    }

    return (
        <main className="container">
            <div className="row">
                <div className="sm-hidden col-md-4"/>
                <Card elevation={Elevation.TWO} className={`${styles.LoginCard} col-md-4`}>
                    <div className="p-sm-3">
                        <form onSubmit={login}>
                            <InputGroup
                                className={errors.length > 0 ? Classes.INTENT_DANGER : ''}
                                leftIcon="user"
                                placeholder="Username"
                                name="username"
                                onChange={handleInputChange}
                            />
                            <InputGroup
                                className={`${styles.PasswordInput} ${errors.length > 0 ? Classes.INTENT_DANGER : ''}`}
                                placeholder="Enter your password..."
                                type="password"
                                name="password"
                                leftIcon="key"
                                onChange={handleInputChange}
                            />
                            <ErrorsDisplay/>
                            <Button type="submit" className={`${styles.LoginButton} ${MINIMAL} ${Classes.INTENT_PRIMARY}`}>Login</Button>
                        </form>
                    </div>
                </Card>
                <div className="md-hidden col-md-4"/>
            </div>
        </main>
    )
}

export default observer(Login);
