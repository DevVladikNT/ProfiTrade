import axios from "axios";
import { useSnackbar } from 'notistack'
import { Card, Flex, Button, TextInput, Text, Title, Metric, Divider} from "@tremor/react";
import React, { useEffect, useState } from "react";

import CompanyAvailable from "./CompanyAvailable";

function Profile(props) {
    const { enqueueSnackbar, closeSnackbar } = useSnackbar();

    const [code, setCode] = useState('');
    const [hint, setHint] = useState(false);
    
    const figi_counters = {};

    const search = () => {
        const getData = async () => {
            const message_ = {
                message: props.device,
                key: code,
            };
            const encrypted_ = await axios.post('http://localhost:2000/encrypt', message_).catch((error) => {
                enqueueSnackbar('Profile\n' + error, {variant: 'error'});
            });
            const token_ = {
                code: code,
                message: encrypted_.data,
            };
            const user_id_ = await axios.put('http://localhost:2000/tokens', token_).catch((error) => {
                enqueueSnackbar('Profile\n' + error, {variant: 'error'});
            });
            const response_ = await axios.get('http://localhost:2000/users/' + user_id_.data).catch((error) => {
                enqueueSnackbar('Profile\n' + error, {variant: 'error'});
            });
            const user_ = response_.data;
            props.setUser(user_);
        };
        getData();
    };

    const onKeyDown= (event) => {
        if (event.key === 'Enter')
            search()
    }

    useEffect(() => {
        props.updatedProfile();
    }, [props]);
    

    return (
        props.user.id === -1 ?
        <Card className="mr-4 mt-4 min-w-[300px] flex flex-col">
            <Title>Profile</Title>
            <Divider />
            <TextInput
                value={code}
                onChange={(event) => setCode(event.target.value)}
                onKeyDown={onKeyDown}
                placeholder="Your code"
            />
            {
                hint ?
                <>
                    <Text className="mt-4 text-center">To get your code use{' '}
                        <a
                            href="https://t.me/profit_trade_bot"
                            target="_blank"
                            rel="noopener noreferrer"
                        >telegram bot</a>
                    </Text>
                </> : <></>
                
            }
            <Divider />
            <Flex>
                <Button
                    variant="secondary"
                    onClick={() => setHint(!hint)}
                >Sign Up</Button>
                <Button onClick={search}>Sign In</Button>
            </Flex>
        </Card> 
        :
        <Card className="mr-4 mt-4 min-w-[300px] flex flex-col">
            <Flex flexDirection="row">
                <Title>Profile</Title>
                <Text>{props.user.username}</Text>
            </Flex>
            <Divider />
            <Metric className="text-center">{Number((props.user.balance).toFixed(2))}</Metric>
            <Divider />
            <div className="min-h-[100px] flex-[1_1_0] flex flex-col overflow-y-auto">
                {props.operations.map((operation) => {
                    operation.figi in figi_counters ?
                    figi_counters[operation.figi] += operation.amount :
                    figi_counters[operation.figi] = operation.amount
                })}
                {Object.keys(figi_counters).map((figi, index) => {
                    return figi_counters[figi] === 0 ?
                    <React.Fragment key={index} /> :
                    <CompanyAvailable
                        key={index}
                        amount={figi_counters[figi]}
                        figi={figi}
                    />
                })}
            </div>
            <Divider/>
            <Button
                variant="secondary"
                onClick={() => props.setUser({id: -1})}
            >Sign Out</Button>
        </Card>
    );
}

export default Profile;