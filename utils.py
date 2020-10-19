import numpy as np

np.random.seed(42)

def format_time(t):
    """Return a formatted time string 'HH:MM:SS
    based on a numeric time() value"""
    m, s = divmod(t, 60)
    h, m = divmod(m, 60)
    return f'{h:0>2.0f}:{m:0>2.0f}:{s:0>2.0f}'


class MultipleTimeSeriesCV:
    """Generates tuples of train_idx, test_idx pairs
    Assumes the MultiIndex contains levels 'symbol' and 'date'
    purges overlapping outcomes"""

    def __init__(self,
                 n_splits=3,
                 train_period_length=126,
                 test_period_length=21,
                 lookahead=None,
                 date_idx='date',
                 symbol_idx = 'Ticker',
                 shuffle=False):
        self.n_splits = n_splits
        self.lookahead = lookahead
        self.test_length = test_period_length
        self.train_length = train_period_length
        self.shuffle = shuffle
        self.date_idx = date_idx
        self.symbol_idx = symbol_idx

    def split(self, X, y=None, groups=None):
        unique_dates = X.index.get_level_values(self.date_idx).unique()
        days = sorted(unique_dates, reverse=True)
        split_idx = []
        date_idx = self.date_idx
        for i in range(self.n_splits):
            test_end_idx = i * self.test_length
            test_start_idx = test_end_idx + self.test_length
            train_end_idx = test_start_idx + self.lookahead - 1
            train_start_idx = train_end_idx + self.train_length + self.lookahead - 1
            split_idx.append([train_start_idx, train_end_idx,
                              test_start_idx, test_end_idx])

        dates = X.reset_index()[[self.date_idx]]
        for train_start, train_end, test_start, test_end in split_idx:
            train_idx = dates[(dates[self.date_idx] > days[train_start])
                              & (dates[date_idx] <= days[train_end])].index
            test_idx = dates[(dates[date_idx] > days[test_start])
                             & (dates[date_idx] <= days[test_end])].index
            if self.shuffle:
                np.random.shuffle(list(train_idx))
            yield train_idx.to_numpy(), test_idx.to_numpy()

    def get_n_splits(self, X, y, groups=None):
        return self.n_splits
    
    def preview_split_dates(self, data):
        date_idx = self.date_idx
        symbol_idx = self.symbol_idx
        for i, (train_idx, test_idx) in enumerate(self.split(X=data)):
            train = data.iloc[train_idx]
            train_dates = train.index.get_level_values(date_idx)
            test = data.iloc[test_idx]
            test_dates = test.index.get_level_values(date_idx)
            df = train.reset_index().append(test.reset_index())
            n = len(df)
            assert n== len(df.drop_duplicates())
            msg = f'Training: {train_dates.min().date()}-{train_dates.max().date()} '
            msg += f' ({train.groupby(symbol_idx).size().value_counts().index[0]:,.0f} days) | '
            msg += f'Test: {test_dates.min().date()}-{test_dates.max().date()} '
            msg += f'({test.groupby(symbol_idx).size().value_counts().index[0]:,.0f} days)'
            print(msg)
            if i == 3:
                break