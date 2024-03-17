from abc import abstractmethod, ABC
from typing import Optional

import numpy as np
import pandas as pd
from player_performance_ratings import ColumnNames


class BaseTransformer(ABC):

    def __init__(self, features: list[str]):
        self.features = features

    @abstractmethod
    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        pass

    @abstractmethod
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        pass

    @property
    @abstractmethod
    def features_out(self) -> list[str]:
        pass


class BasePostTransformer(ABC):

    def __init__(self, features: list[str], are_estimator_features: bool = True):
        self.features = features
        self._are_estimator_features = are_estimator_features
        self._features_out = []
        self.column_names = None

    @abstractmethod
    def fit_transform(self, df: pd.DataFrame, column_names: ColumnNames) -> pd.DataFrame:
        pass

    @abstractmethod
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        pass

    @property
    def features_out(self) -> list[str]:
        return self._features_out

    @property
    def estimator_features_out(self) -> list[str]:
        if self._are_estimator_features:
            return self.features_out
        return []

    def reset(self):
        pass


class BaseLagTransformer(BasePostTransformer):

    def __init__(self,
                 granularity: list[str],
                 features: list[str],
                 add_opponent: bool,
                 iterations: list[int],
                 prefix: str,
                 are_estimator_features: bool = True,
                 ):
        super().__init__(features, are_estimator_features)
        self.granularity = granularity
        if isinstance(self.granularity, str):
            self.granularity = [self.granularity]
        self._entity_features = []
        self.add_opponent = add_opponent
        self.prefix = prefix
        self._df = None
        self._entity_features = []
        self._fitted_game_ids = []

        for feature_name in self.features:
            for lag in iterations:
                self._features_out.append(f'{prefix}{lag}_{feature_name}')
                self._entity_features.append(f'{prefix}{lag}_{feature_name}')
                if self.add_opponent:
                    self._features_out.append(f'{prefix}{lag}_{feature_name}_opponent')

    def _concat_df(self, df: pd.DataFrame, additional_cols_to_use: Optional[list[str]] = None) -> pd.DataFrame:
        df = self._string_convert(df=df)
        for feature in self.features:
            if feature in df.columns:
                df = df.assign(**{feature: lambda x: x[feature].astype('float')})

        cols = [f for f in list(
            set([*self.features, *self.granularity, self.column_names.match_id, self.column_names.team_id,
                 self.column_names.player_id,
                 self.column_names.parent_team_id, self.column_names.update_match_id,
                 self.column_names.start_date])) if f in df.columns]

        if additional_cols_to_use:
            cols += [f for f in additional_cols_to_use if f in df.columns]

        concat_df = pd.concat([self._df, df[cols]], axis=0).reset_index()

        if 'index' in concat_df.columns:
            concat_df = concat_df.drop(columns=['index'])
        if concat_df[self.column_names.start_date].dtype in ('str', 'object'):
            concat_df[self.column_names.start_date] = pd.to_datetime(concat_df[self.column_names.start_date])
        return concat_df.drop_duplicates(
            subset=[self.column_names.match_id, self.column_names.team_id, self.column_names.player_id], keep='last')

    def _fit_transform(self, df: pd.DataFrame, additional_cols_to_use: Optional[list[str]] = None) -> pd.DataFrame:
        df = self._string_convert(df)

        cols = list(
            set([*self.features, *self.granularity, self.column_names.match_id, self.column_names.team_id,
                 self.column_names.player_id,
                 self.column_names.parent_team_id, self.column_names.update_match_id,
                 self.column_names.start_date]))

        if additional_cols_to_use:
            cols += additional_cols_to_use

        if self._df is None:
            self._df = df[cols]
        else:
            self._df = pd.concat([self._df, df[cols]], axis=0)

        self._df = self._df.drop_duplicates(
            subset=[self.column_names.match_id, self.column_names.team_id, self.column_names.player_id], keep='last')

        transformed_df = self.transform(df=df)
        self._fitted_game_ids = list(set(transformed_df[self.column_names.match_id].tolist() + self._fitted_game_ids))
        return transformed_df

    def _string_convert(self, df: pd.DataFrame) -> pd.DataFrame:
        for column in [self.column_names.match_id, self.column_names.parent_team_id, self.column_names.player_id,
                       self.column_names.update_match_id]:
            df = df.assign(**{column: lambda x: x[column].astype('str')})
        return df

    def _create_transformed_df(self, df: pd.DataFrame, concat_df: pd.DataFrame, exclude_features: Optional[list[str]] = None) -> pd.DataFrame:

        exclude_features = exclude_features or []

        #  for feat in feats_added:
        #     concat_df['is_ori_nan'] = concat_df[feat].isna().astype(int)
        #     if feat in feats_to_forward_fill_future_periods:
        # concat_df.loc[~(concat_df[self.column_names.match_id].isin(self._fitted_game_ids)) & (concat_df[self.column_names.start_date] >= max_date_fitted) & (concat_df[feat]==0), feat] = np.nan
        #         concat_df.loc[~(concat_df[self.column_names.match_id].isin(self._fitted_game_ids)) & (concat_df[feat] == 0), feat] = np.nan
        #      concat_df[feat] = concat_df.groupby(self.granularity)[feat].fillna(method='ffill')
        #      concat_df.loc[(concat_df['is_ori_nan'] == 1) &(df[self.column_names.match_id].isin(self._fitted_game_ids)) , feat] = np.nan

        cn = self.column_names

        unfitted_game_ids = False
        if len(self._df[cn.match_id].unique()) != len(set(df[cn.match_id].unique().tolist() + self._fitted_game_ids)):
            unfitted_game_ids = True

        if self.add_opponent and not unfitted_game_ids:
            concat_df = self._add_opponent_features(df=concat_df)

        ori_cols = [c for c in df.columns if c not in concat_df.columns] + [cn.match_id, cn.player_id, cn.team_id]
        ori_index_values = df.index.tolist()

        df = self._string_convert(df)

        transformed_df = concat_df.merge(df[ori_cols],
                                         on=[cn.match_id, cn.player_id, cn.team_id], how='inner')

        if unfitted_game_ids:
            transformed_df[self._entity_features] = transformed_df[self._entity_features].fillna(-999.21345)
            first_grp = transformed_df.groupby(self.granularity)[self._entity_features].first().reset_index()
            transformed_df = transformed_df[
                [c for c in transformed_df.columns if c not in self._entity_features]].merge(first_grp,
                                                                                             on=self.granularity,
                                                                                             how='left')
            for f in self._entity_features:
                transformed_df[f].replace(-999.21345, np.nan, inplace=True)
            transformed_df.groupby(self.granularity)[self._entity_features].fillna(method='ffill', inplace=True)

            team_features = transformed_df.groupby([self.column_names.team_id, self.column_names.match_id])[
                self._entity_features].mean().reset_index()
            df_opponent_feature = team_features.rename(
                columns={**{self.column_names.team_id: '__opponent_team_id'},
                         **{f: f"{f}_opponent" for f in self._entity_features}}
            )
            opponent_feat_names = [f"{f}_opponent" for f in self._entity_features]
            new_df = transformed_df.merge(df_opponent_feature, on=[self.column_names.match_id],
                                          suffixes=('', '_team_sum'))
            new_df = new_df[new_df[self.column_names.team_id] != new_df['__opponent_team_id']]
            new_df[opponent_feat_names] = new_df[
                opponent_feat_names].fillna(-999.21345)
            first_grp = new_df.groupby('__opponent_team_id')[
                opponent_feat_names].first().reset_index()
            new_df = new_df[
                [c for c in new_df.columns if c not in opponent_feat_names]].merge(first_grp,
                                                                                   on='__opponent_team_id',
                                                                                   how='left')
            for f in opponent_feat_names:
                new_df[f].replace(-999.21345, np.nan, inplace=True)

            new_df = new_df.sort_values(by=[cn.start_date, cn.match_id,'__opponent_team_id'])
            new_df.groupby('__opponent_team_id')[opponent_feat_names].fillna(method='ffill',
                                                                             inplace=True)

            transformed_df = transformed_df.merge(
                new_df[[self.column_names.match_id, self.column_names.team_id, self.column_names.player_id,
                        *opponent_feat_names]],
                on=[self.column_names.match_id, self.column_names.team_id, self.column_names.player_id], how='left')

        transformed_df.index = ori_index_values
        transformed_df = transformed_df.sort_values(by=[cn.start_date, cn.match_id,
                                                        cn.team_id, cn.player_id])
        return_feats = [f for f in self.features_out if f not in exclude_features]
        return transformed_df[list(set(df.columns.tolist() + return_feats))]

    def _add_opponent_features(self, df: pd.DataFrame) -> pd.DataFrame:
        team_features = df.groupby([self.column_names.team_id, self.column_names.match_id])[
            self._entity_features].mean().reset_index()
        df_opponent_feature = team_features.rename(
            columns={**{self.column_names.team_id: '__opponent_team_id'},
                     **{f: f"{f}_opponent" for f in self._entity_features}}
        )
        new_df = df.merge(df_opponent_feature, on=[self.column_names.match_id], suffixes=('', '_team_sum'))
        new_df = new_df[new_df[self.column_names.team_id] != new_df['__opponent_team_id']].drop(
            columns=['__opponent_team_id'])

        new_feats = [f"{f}_opponent" for f in self._entity_features]
        return df.merge(
            new_df[[self.column_names.match_id, self.column_names.team_id, self.column_names.player_id,
                    *new_feats]],
            on=[self.column_names.match_id, self.column_names.team_id, self.column_names.player_id], how='left')

    def reset(self):
        self._df = None
