import axios from 'axios'
import { Card, Flex, Text, Title, Metric, NumberInput, BadgeDelta, AreaChart, Divider, Button } from "@tremor/react";
import { useEffect, useState } from 'react';

function PricePlot(props) {
    const [can_update, setCanUpdate] = useState(true);
    const [buy_amount, setBuyAmount] = useState('');

    const [history, setHistory] = useState([]);
    const [price, setPrice] = useState(0);
    const [growth, setGrowth] = useState(0);
    const [direction, setDirection] = useState('moderateIncrease');

    const [pred, setPred] = useState(0);
    const [pred_growth, setPredGrowth] = useState(0);
    const [pred_direction, setPredDirection] = useState('moderateIncrease')

    useEffect(() => {
        const getData = async () => {
            const response_ = await axios.get('http://localhost:2000/prices/' + props.company.figi);
            const history_ = response_.data.response;
            setHistory(history_);
            setPrice(history_[history_.length - 1].close)
            const prediction_ = await axios.post('http://localhost:3000/predict', {'input': history_});
            const pred_ = prediction_.data.response;
            setPred(pred_);

            const diff_ = (history_[history_.length - 1].close - history_[history_.length - 2].close) / history_[history_.length - 2].close;
            const growth_ = Number((diff_ * 100).toFixed(2));
            setGrowth(growth_);
            const dir_ = growth_ > 0 ? "moderateIncrease" : "moderateDecrease";
            setDirection(dir_);

            const pred_diff_ = (pred_ - history_[history_.length - 1].close) / history_[history_.length - 1].close;
            const pred_growth_ = Number((pred_diff_ * 100).toFixed(2));
            setPredGrowth(pred_growth_);
            const pred_dir_ = pred_growth_ > 0 ? "moderateIncrease" : "moderateDecrease";
            setPredDirection(pred_dir_);
        };

        getData();
    }, [props]);

    useEffect(() => {
        const prices = setInterval(async () => {
            const response_ = await axios.get('http://localhost:2000/prices/' + props.company.figi);
            const history_ = response_.data.response;
            setHistory(history_);
            setPrice(history_[history_.length - 1].close)
            const prediction_ = await axios.post('http://localhost:3000/predict', {'input': history_});
            const pred_ = prediction_.data.response;
            setPred(pred_);

            const diff_ = (history_[history_.length - 1].close - history_[history_.length - 2].close) / history_[history_.length - 2].close;
            const growth_ = Number((diff_ * 100).toFixed(2));
            setGrowth(growth_);
            const dir_ = growth_ > 0 ? "moderateIncrease" : "moderateDecrease";
            setDirection(dir_);

            const pred_diff_ = (pred_ - history_[history_.length - 1].close) / history_[history_.length - 1].close;
            const pred_growth_ = Number((pred_diff_ * 100).toFixed(2));
            setPredGrowth(pred_growth_);
            const pred_dir_ = pred_growth_ > 0 ? "moderateIncrease" : "moderateDecrease";
            setPredDirection(pred_dir_);
        }, 10000);

        return () => {
            clearInterval(prices);
        };
    }, [props]);

    useEffect(() => {
        setTimeout(() => setCanUpdate(true), 2000);
    }, [can_update]);

    const handlerClick = (event) => {
        if (event.target.textContent == 'Buy') {
            console.log(`Bought`);
        } else if (event.target.textContent == 'Sell') {
            console.log(`Sold`);
        }
        setBuyAmount('');
        props.needUpdateOperations();
    };

    const handlerMouseEnter = (event) => {
        if (!can_update)
            return;
        setCanUpdate(false);
        const getData = async () => {
            let response_ = await axios.get('http://localhost:2000/close_price/' + props.company.figi);
            let price_ = response_.data.response;
            setPrice(price_);
        };
        getData();
    };

    return (
        <Flex flexDirection='col'>
            <Card>
                <Flex flexDirection='row'>
                    <Title>{props.company.name}</Title>
                    <BadgeDelta deltaType={direction}>{Math.abs(growth)}%</BadgeDelta>
                </Flex>
                <Divider>{props.company.ticker}</Divider>
                <AreaChart
                    className="h-72 mt-4"
                    data={history}
                    index="time"
                    categories={["close"]}
                    colors={["indigo"]}
                    yAxisWidth={40}
                    showXAxis={false}
                    showLegend={false}
                    autoMinValue={true}
                />
                <Divider>Prediction</Divider>
                <Flex flexDirection='row'>
                    <Metric>{pred}</Metric>
                    <BadgeDelta deltaType={pred_direction}>{Math.abs(pred_growth)}%</BadgeDelta>
                </Flex>
            </Card>
            <Card className="mt-4">
                <Flex flexDirection="row">
                    <Metric className="mr-4">{price}</Metric>
                    <NumberInput
                        placeholder="Amount"
                        min={0}
                        value={buy_amount}
                        onChange={(event) => setBuyAmount(event.target.value)}
                    />
                    <Button
                        className="ml-4"
                        variant="secondary"
                        onClick={handlerClick}
                        onMouseEnter={handlerMouseEnter}
                    >Sell</Button>
                    <Button
                        className="ml-4"
                        onClick={handlerClick}
                        onMouseEnter={handlerMouseEnter}
                    >Buy</Button>
                </Flex>
            </Card>
        </Flex>
    );
}

export default PricePlot;